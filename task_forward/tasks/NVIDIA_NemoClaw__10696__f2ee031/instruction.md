# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Remove Shields from NemoClaw core and defer immutability to composable blueprints

## Problem

NemoClaw currently owns an opt-in post-provisioning immutability system called Shields. The host CLI captures and rewrites live policy, changes agent configuration and state-directory ownership and modes, manages timers and rollback state, coordinates gateway and runtime-provider mutations, verifies the resulting posture, and carries recovery logic across backup, rebuild, snapshot, MCP, messaging, inference, and destructive lifecycle operations.

That is the wrong long-term product boundary. NemoClaw should orchestrate agents on OpenShell, integrate inference and credentials, and manage the lifecycle of the resources it creates. It should not be the product that owns post-provisioning immutability of agent-controlled configuration or state.

Immutability remains a valid optional capability. Ecosystem products may provide it later as a composable blueprint or overlay applied on top of NemoClaw. If users strongly value the current behavior, a future community example may reintroduce it outside NemoClaw core. This issue does not pre-design that future extension or require NemoClaw to retain Shields-shaped abstractions for it.

Issue #10514 remains authoritative for making OpenShell the sole durable policy source of truth. This decision supersedes only its requirements that Shields remain supported and that the Shields command surface be preserved.

## Product decision

Status: **Accept**

- **Reason:** Agent-state immutability is an optional ecosystem capability, not an inherent NemoClaw responsibility. Keeping it in core creates substantial cross-cutting security, lifecycle, recovery, image, provider, and qualification machinery that every supported agent must carry.
- **Placement:** NemoClaw core supports mutable agent configuration and state inside the OpenShell sandbox. OpenShell continues to own and enforce sandbox policy and isolation. Optional post-provisioning immutability belongs in independently owned ecosystem products or composable blueprints.
- **Accountable maintainer:** @ericksoa
- **Validation:** Focused source and integration tests, CLI/plugin type checks, repository checks, docs build, exact affected live E2E for each supported agent and lifecycle flow, then the complete supported pull-request E2E matrix on the exact candidate commit.

## Architectural rule

NemoClaw core must not own a product concept, state machine, provider surface, manifest contract, qualification contract, or public command for post-provisioning immutability of agent configuration or state.

This rule does not prohibit immutable resource identities, digests, exact-generation fencing, signed or qualified artifacts, or other control-plane integrity mechanisms. Those remain required where they establish authority over resources NemoClaw manages.

## Required behavior

### Remove the public Shields surface

- Remove `sandbox shields up`, `sandbox shields down`, and `sandbox shields status` plus public aliases.
- Remove the in-sandbox plugin guidance/status surface for Shields.
- Remove Shields flags, timeout parsing, reasons, policy selection, status presentation, audit warnings, and documentation.
- Remove command guidance that directs users to lower or raise Shields.

### Remove core ownership and persisted state

- Remove the host Shields coordinator, timer process, transition locks, timer-bound locks, policy snapshots/deltas, rollback state, seals, status state, audit events, recovery artifacts, and verification code.
- Remove Shields-specific fields from agent manifests and derived agent definitions, including protected/confidential path declarations and in-image state-lock-plan selection.
- Remove generated state-lock plans and the descriptor-safe state-directory guard when they have no remaining non-Shields responsibility.
- Remove Shields-specific branches from policy, config, inference, messaging, MCP, snapshot, backup, restore, clone, rebuild, destroy, start, connect, doctor, status, and lifecycle locking.
- Stop persisting or interpreting local Shields state after the bounded compatibility transition described below.

### Remove orphaned runtime-provider machinery

- Remove the runtime-provider `stateMutation` contract, Docker implementation, dormant Podman candidate implementation, persisted engine mutation lifecycle, Hermes publisher/controller/startup-gate protocol, image capability descriptor, and associated activation/qualification wiring when the final import graph confirms there is no non-Shields production consumer.
- Do not retain this machinery for a hypothetical future immutability product.
- Preserve unrelated persisted engine authority used by managed inference and other active runtime-provider features.

### Preserve the actual NemoClaw and OpenShell boundaries

- Keep OpenShell policy authoritative. Preserve NemoClaw policy convenience commands and their live read-modify-write behavior.
- Keep OpenShell filesystem and network enforcement, credential providers and rewriting, redaction, SSRF controls, sandbox identity checks, provider identity checks, lifecycle generation fencing, gateway lifecycle controls, MCP resource lifecycle, backup/restore correctness, and managed-inference integrity.
- Keep config schema validation, atomic config writes, restart seals, startup readiness, MCP integrity, and credential-boundary guards where they have a non-Shields responsibility. Split or rename mixed helpers rather than deleting those responsibilities.
- Keep the generic per-sandbox mutation lock for active lifecycle, policy, channel, snapshot, inference, session, and MCP operations. Remove only its Shields timer/deadline/containment behavior and obsolete compatibility state.

### Simplify dependent workflows

- Snapshot and backup no longer require or open a Shields-down window.
- Rebuild, restore, clone, and destroy no longer preserve or restore a Shields posture.
- Config, inference, MCP, messaging, and channel operations no longer reject mutation because Shields are up.
- Agent config and state restored into a new or rebuilt sandbox use the supported mutable posture.
- Status and doctor report real remaining policy, filesystem, credential, lifecycle, and runtime health without a Shields posture.

## Existing-sandbox transition

The removal must not silently strand an existing sandbox in a root-owned, immutable, timed-down, or partially transitioned Shields posture.

- Detect registered sandboxes and host state that still carry Shields state or recovery artifacts.
- For a posture that can be proven and safely converted, perform one bounded conversion to the supported mutable posture and remove the exact matching host artifacts only after verification.
- If safe in-place conversion cannot be proven, stop with explicit backup/rebuild/recreate guidance. Never delete ambiguous timer, transition, lock, or containment generations and never claim the sandbox is mutable without verification.
- A sandbox rebuilt or recreated from retained user state must not restore Shields ownership, modes, immutable flags, timers, policy deltas, or host state.
- Do not ship a compatibility subsystem that leaves the core concept partially supported. If safe in-place conversion cannot complete within this change, require the explicit rebuild or recreate path instead.

## Ecosystem and community boundary

- Do not move Shields into a bundled community example as part of this issue.
- Do not add a generic core hook, provider contract, or blueprint API solely to preserve the old implementation shape.
- If concrete ecosystem demand appears later, design the smallest composable blueprint boundary from that real consumer.
- A future community example must own its protected-path declarations, helpers, apply/remove/recovery behavior, tests, documentation, compatibility, and support posture outside NemoClaw core.

## Delivery constraints

- Deliver the complete semantic cutover in one pull request. Do not split command removal, core deletion, runtime-provider deletion, image changes, migration behavior, tests, or documentation across separate pull requests.
- Do not merge a state where any agent or lifecycle flow still treats Shields as supported while another surface has removed its commands or recovery authority.
- The completed source-and-test change must be substantially net-negative.
- Remove implementation-shaped tests with the implementation. Retain and update outcome tests for the security and lifecycle boundaries that remain.
- Update user documentation and security positioning to state that NemoClaw does not provide post-provisioning agent-state immutability.
- Do not weaken an unrelated security control merely because it currently lives in a mixed Shields helper.

## Acceptance evidence

### Source and contracts

- No public Shields command, alias, plugin route, flag, status, or documentation remains.
- No production module imports `src/lib/shields`, Shields timer authority, Shields transition locks, or the runtime-provider `stateMutation` surface.
- Agent manifests contain backup/restore state semantics without Shields protection semantics.
- The production runtime-provider registry and activation contract contain no unused `stateMutation` capability.
- Repository searches find no product-facing Shields terminology outside changelog/history or explicitly bounded migration diagnostics.

### Behavior

- OpenClaw, Hermes, Deep Agents Code, Pi, and other supported agents onboard into the mutable posture without Shields artifacts.
- Config, inference, policy, MCP, messaging, channels, snapshot, backup, restore, clone, rebuild, start/stop, destroy, doctor, and status work without Shields gates.
- Existing live OpenShell policy and unrelated host policy changes survive every affected operation.
- Credential values remain absent from agent config and diagnostics; credential injection and rewriting still pass their existing security tests.
- Existing locked, timed-down, interrupted, and clean mutable sandbox fixtures either convert safely or produce the documented recreate path without ambiguous cleanup.
- Rebuild and recreate never rematerialize Shields state.

### Qualification

- Focused tests and type checks pass.
- `npx prek run --all-files` passes.
- `npm test` passes.
- Documentation builds without warnings.
- Exact affected live E2E passes for OpenClaw, Hermes, Deep Agents Code, and every lifecycle scenario changed by the cutover.
- The complete supported pull-request E2E matrix passes at the exact candidate commit.

## Non-goals

- Remove or weaken OpenShell policy enforcement.
- Remove mutable-state backup, restore, or migration semantics.
- Remove immutable identities, digests, exact-target authority, or qualification evidence used by active NemoClaw-managed resources.
- Design or ship the future ecosystem immutability product.
- Preserve the current Shields architecture under a new core name.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f2ee031ffae355e2cc8bc5cb785f0c6f582f4ac9`.  There
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
{"case_id": "NVIDIA_NemoClaw__10696__f2ee031",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
