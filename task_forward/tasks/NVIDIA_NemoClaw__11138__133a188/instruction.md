# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Security] unresolvable sandbox base image override is accepted silently instead of failing closed

## Description

A sandbox base image override that cannot be resolved to a registry digest is accepted silently instead of failing closed. Tagging an unrelated local image with a name inside the trusted `sandbox-base` repository and passing it as `NEMOCLAW_SANDBOX_BASE_IMAGE_REF` makes onboarding exit 0 and create a working sandbox, with no rejection message anywhere in the output.

The created sandbox does not run the substituted content — its container is the normal Debian base with the OpenShell supervisor present — so the override appears to be ignored rather than honoured. Either way the documented contract is not met: an override that resolves to no immutable trusted digest is supposed to abort onboarding.

**Two readings are possible and this report does not assume either.** The resolution path may be failing open, or the override may no longer govern the image the current pipeline uses at all — the created sandbox image carries `io.nvidia.nemoclaw.managed-image.*` labels, which suggests a managed-image path that may not consult this variable. The variable itself is still live in the product: `src/lib/onboard/base-image.ts` passes `envVar: "NEMOCLAW_SANDBOX_BASE_IMAGE_REF"` to `resolveSandboxBaseImage`, whose override branch is written to throw when no digest is produced.

Dev input is needed on which of the two it is, because the difference decides whether a trust boundary is open or whether documentation and QA are asserting a control that has been retired.

- **Platform scope:** Reproduced on Ubuntu 24.04 x86_64; other platforms not tested by this run.
- **Regression:** Unknown — earlier releases were not tested for this path.
- **OpenShell issue:** No. The resolution and rejection logic is NemoClaw's own.

## Environment

```text
Device:        Ubuntu 24.04 x86_64 workstation with an NVIDIA GeForce RTX 5090 D
OS:            Ubuntu 24.04.4 LTS
Architecture:  x86_64
Kernel:        6.17.0-23-generic
Node.js:       v22.23.0
npm:           10.9.8
Docker:        Docker version 29.7.2, build a7dcaa6
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.118
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. Remove any previously built sandbox image so base resolution cannot be skipped by reuse, and confirm with `docker images` that none remains.

   ```bash
   docker image rm -f $(docker images -q ghcr.io/nvidia/nemoclaw/openclaw-sandbox)
   ```

2. Create a local-only tag inside the trusted repository whose content is unrelated and which was never published, so it has no registry digest.

   ```bash
   docker pull alpine:3.20
   docker tag alpine:3.20 ghcr.io/nvidia/nemoclaw/sandbox-base:local-only-no-push
   ```

3. Onboard with that tag as the base image override.

   ```bash
   NEMOCLAW_SANDBOX_BASE_IMAGE_REF=ghcr.io/nvidia/nemoclaw/sandbox-base:local-only-no-push \
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_YES=1 NEMOCLAW_PROVIDER=build \
     nemoclaw onboard --name <sandbox> --yes
   ```

4. Check whether the sandbox was created and what it is actually running.

   ```bash
   nemoclaw list
   docker exec <sandbox container> sh -c 'head -2 /etc/os-release; ls /opt/openshell/bin/'
   ```

## Expected Result

Step 3 exits non-zero and reports that the override could not be resolved to an immutable trusted digest, or that it failed the required compatibility checks. No sandbox is created, and step 4 shows the name absent from the sandbox list.

## Actual Result

Step 3 exits 0 and reports the sandbox created. Nothing in the output mentions the override, a digest, a pull attempt or a rejection; searching the full onboarding output for `could not be resolved`, `immutable trusted digest`, `compatibility checks` and `outside the trusted` returns no match at all.

Step 4 lists the sandbox, and its container reports the legitimate Debian base with the OpenShell supervisor present — so the substituted Alpine content is not what runs; the override is silently disregarded rather than refused.

## Logs

```text
onboard exit code: 0
rejection wording search over the full onboarding output: no match

nemoclaw list: the sandbox is present

container inspection:
  PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
  NAME="Debian GNU/Linux"
  openshell-sandbox
```

## Related issues — neither is a duplicate

- #7058 (closed) — digest validation intermittently **rejected** an official release-tag image. If that was resolved by relaxing validation, this report may be the same boundary moving the other way, and the two should be considered together rather than in isolation.
- #7609 (closed) — a failed untrusted base-image onboarding left ghost sandbox entries. That report covers the aftermath of a rejection actually happening; here no rejection happens.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `133a1886c318a45adc0a979cc1e6ebfc407bf066`.  There
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
{"case_id": "NVIDIA_NemoClaw__11138__133a188",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
