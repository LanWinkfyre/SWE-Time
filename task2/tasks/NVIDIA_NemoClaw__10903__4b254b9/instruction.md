# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Upgrade recovery forces local Hermes base rebuild when legacy managed sandbox lacks resolution metadata

## Description

A supported installer upgrade from the stock `lkg` Hermes path at v0.0.109 to v0.0.118 attempted to recover an existing managed sandbox. The release already publishes and pins an exact validated Hermes base image, but recovery forced a local `agents/hermes/Dockerfile.base` build because the existing sandbox image did not yield a reusable base-image resolution hint.

That local build introduced avoidable source-network dependencies. In the observed run, APT completed and the native security builder then exhausted all six `curl` attempts while fetching the checksum-pinned libssh2 source from `https://libssh2.org/download/libssh2-1.11.1.tar.xz`:

```text
Rebuilding Hermes Agent base image...
...
curl: (35) Recv failure: Connection reset by peer
(repeated for all retry attempts)
...
Rebuild preflight failed: agent base image could not be built.
Sandbox is untouched — no data was lost.
Failed to recover 'clawgilly': Failed to build Hermes Agent base image (exit 1)
```

The transport reset may be host/network-specific. The NemoClaw defect is that a qualified managed release upgrade entered a network-dependent local compilation path even though the release's immutable published Hermes base was available.

The original sandbox remained intact because failure occurred during rebuild preflight. The v0.0.118 CLI installation completed, but automatic sandbox recovery did not.

### Expected behavior

For a sandbox that the upgrade preflight positively qualifies as NemoClaw-managed, absence of cached base-image resolution metadata should be treated as a cache/provenance miss. It should not by itself authorize or force a local source build.

Recovery should resolve, pull, and validate the current release's exact pinned Hermes base image before any destructive sandbox mutation. If source-workload ownership cannot be established or the exact release image cannot be resolved and validated, recovery must fail closed with actionable guidance and leave the sandbox untouched.

## Reproduction Steps

Observed supported sequence:

1. Install/onboard stock Hermes from `lkg` v0.0.109 on an Ubuntu OmniStation host, using non-default gateway port `8990` to coexist with a pre-existing OpenShell service.
2. Use the official immutable v0.0.109 Hermes base digest through the supported `NEMOCLAW_HERMES_SANDBOX_BASE_IMAGE_REF` override during onboarding. The sandbox is created successfully and remains registered as managed; no custom Dockerfile is used.
3. Enter a supported rebuild/recovery flow. The immediate trigger in this report was the Hermes MCP integrity quarantine family tracked by #8649.
4. Upgrade through the maintained installer with `NEMOCLAW_INSTALL_TAG=v0.0.118` and `NEMOCLAW_GATEWAY_PORT=8990` preserved.
5. Observe installer-driven recovery call the rebuild path.
6. Because `readSandboxBaseImageResolutionMetadata(sandboxEntry.imageTag)` supplies no usable hint, observe `ensureRebuildAgentBaseImage()` set `forceBaseImageRebuild: true` and execute `agents/hermes/Dockerfile.base` locally.
7. Make `libssh2.org` unreachable or reset TLS connections. Observe recovery fail even though the v0.0.118 Dockerfile pins the published Hermes base index `sha256:d30f58b0374c7d281df07c126cc257baaf63eb051264a575b96099ec037d5e5d`.

A focused automated reproducer can construct a positively qualified legacy managed Hermes registry/image fixture without base-resolution metadata, then run installer-driven recovery with the source-download host denied.

## Environment

- Platform: NVIDIA OmniStation, Ubuntu Linux, remote SSH session
- Container runtime: Docker driver
- Source NemoClaw: v0.0.109 (`lkg`)
- Target NemoClaw: v0.0.118
- Node.js: v22.23.2
- OpenShell before upgrade: v0.0.101
- Hermes Agent: v0.19.0
- Gateway: `nemoclaw-8990` (`NEMOCLAW_GATEWAY_PORT=8990`)
- Sandbox: CPU Hermes sandbox
- Custom Dockerfile: none
- Exact OS and Docker versions were not collected

No credentials, provider secrets, usernames, hostnames, or private endpoints are included in this report.

## Current code path

Current `main` commit inspected: `8c974afaa6e92b6480a4bc8b11eb918616851b44`.

`src/lib/actions/sandbox/rebuild-flow-helpers.ts` currently chooses:

```ts
forceBaseImageRebuild: !hasExplicitOverride && !options.resolutionHint
```

This makes a missing resolution hint sufficient to force local compilation. The hint is obtained from the existing sandbox image, so missing, retired, or legacy image metadata selects the local-build path even when the source sandbox has independently passed managed-workload qualification.

The Hermes resolver already supports the desired target behavior: `createAgentBaseImageResolutionOptions()` carries the Dockerfile-pinned remote reference, requires that pinned remote reference, and validates the MCP/ACP runtime capabilities, immutable security inventory, platform, and OpenShell ABI.

## Proposed Design

### 1. Separate source authority from target base-image selection

Do not use `resolutionHint` presence as a proxy for either source ownership or local-build authorization.

During rebuild preflight, determine these independently:

- **Source workload authority:** whether NemoClaw may preserve state from and replace the existing sandbox. Continue using the current managed workload receipt/fingerprint, `fromDockerfile` exclusion, exact live identity checks, and the existing explicit legacy-managed confirmation path where required.
- **Target base intent:** how the replacement base must be obtained.

Introduce an explicit target intent such as:

```ts
type RebuildBaseIntent =
  | { kind: "release-pinned" }
  | { kind: "trusted-local-rebuild"; provenance: LocalBuildProvenance }
  | { kind: "explicit-override"; ref: string };
```

A missing resolution hint is only a cache miss. It must not select `trusted-local-rebuild`.

### 2. Use `release-pinned` for qualified stock/managed upgrades

When installer-driven recovery has positively qualified the source sandbox as managed and it has no custom Dockerfile intent:

1. Select `release-pinned` even when the old image has no resolution metadata.
2. Resolve the exact immutable base reference declared by the target release.
3. Require the existing Hermes validations: official repository, immutable digest, platform, OpenShell ABI, MCP Streamable HTTP/ACP support, and security inventory.
4. Pull/inspect the image and establish the existing operation-scoped trusted remote lease before deletion or recreation.
5. Pass that exact resolution metadata through the final-image build and persist it on the replacement image.

This trusts only the target release's reviewed immutable artifact; it does not infer trust from an arbitrary legacy or local image.

### 3. Keep local compilation explicit and provenance-bound

Select `trusted-local-rebuild` only when one of the existing trusted local-build contracts positively requires it, for example:

- a durable repository-built local provenance receipt that still matches the current source inputs;
- an explicit supported operator/developer local-build request; or
- another existing local-build authority that supplies the in-memory trust lease.

An absent/stale hint, registry pull failure, catalog failure, or validation failure must not fall back to source compilation.

Custom-image sandboxes remain outside automatic stock-image replacement. Ambiguous legacy ownership must continue to fail closed or use the existing exact-name managed-recreate confirmation; confirmation qualifies source replacement but does not make the old base trusted.

### 4. Resolve the target before destructive mutation

The pinned image must be pulled, inspected, and fully validated during rebuild preflight. Any registry, platform, ABI, capability, or security-inventory failure must leave the existing sandbox and registry untouched.

After successful recreation, persist the new resolution metadata so subsequent warm rebuilds use the normal validated hint path.

### 5. Make the selected path observable

Print one explicit, non-secret diagnostic before mutation:

- `Using release-pinned Hermes base image: <immutable ref>`; or
- `Rebuilding trusted local Hermes base image: <provenance class>`.

If an explicitly authorized local build fails during a source download, identify the public source URL/host and curl failure class. Do not add unbounded retries or weaken checksum validation.

## Acceptance Criteria

- [ ] Installer-driven recovery of a positively qualified managed Hermes sandbox with no base-resolution hint uses the target release's exact published base image.
- [ ] That path does not execute `agents/hermes/Dockerfile.base` or contact `libssh2.org`.
- [ ] The pinned remote image passes the existing repository, digest, platform, ABI, MCP/ACP, and security-inventory checks before sandbox deletion.
- [ ] The replacement preserves the sandbox name, gateway binding/port, policy, inference configuration, and manifest-declared Hermes state.
- [ ] Successful replacement persists reusable resolution metadata.
- [ ] Missing or invalid published-image evidence fails before mutation and never falls back to local compilation.
- [ ] An ambiguous/custom legacy sandbox is not silently converted to the stock managed image.
- [ ] Existing explicit, provenance-bound local rebuild behavior remains supported.
- [ ] Tests cover v0.0.109-style missing metadata, explicit legacy-managed confirmation, custom/ambiguous refusal, unavailable pinned image, explicit trusted local build, and non-default gateway port preservation.
- [ ] An integration test denies `libssh2.org` and proves the qualified managed upgrade still succeeds through the published image.

## Related Work

- #8649 tracks the Hermes integrity quarantine/recovery family that triggered the rebuild in this observation; it does not own target base-image selection.
- #4680 introduced cached/prefetched base-image resolution and explicit refresh behavior.
- #10357 fixed the earlier Trixie OpenSSL package mismatch in local managed-image builds, but does not prevent this unnecessary local build path.
- #9822 handles bounded GitHub HTTP 429 retries for a different Hermes source archive. It should not be broadened into generic transport retries for this issue.

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4b254b9bef3e0ba745af4859fc65700742f5317e`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "NVIDIA_NemoClaw__10903__4b254b9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
