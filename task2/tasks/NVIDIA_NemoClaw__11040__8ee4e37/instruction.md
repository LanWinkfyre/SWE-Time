# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Onboard] vLLM automatic preset selection fails with a generic message when GPU memory is insufficient

## Description

On N1x Linux with GPU memory below the vLLM recipe's minimum requirement, automatic vLLM inference-provider selection during onboarding fails with a generic error that gives no indication of why, even though the system internally computes a precise reason before discarding it. Onboarding aborts with no actionable information for the user.

Platform scope: Reproduced on N1x Linux only; other platforms not tested.
Regression: Unknown — earlier versions not tested for this exact message.
OpenShell issue: No

## Environment

```text
Device:        N1x Linux Laptop (RTX Spark N1X, aarch64)
OS:            Ubuntu 24.04.4 LTS (aarch64)
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        server 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. On N1x Linux with GPU memory below the vLLM recipe's minimum requirement, run:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 NEMOCLAW_PROVIDER=install-vllm NEMOCLAW_YES=1 NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 NEMOCLAW_NON_INTERACTIVE_SUDO_MODE=prompt bash
   ```
2. Onboarding proceeds non-interactively through preflight (all checks pass) and reaches "[3/8] Configuring inference provider", Provider: install-vllm

Note: the identical failure also reproduces via the ordinary interactive path — accepting the default N1x Express `[Y/n]` prompt with `Y`, no flags or overrides — which reaches the same step and produces the same error.

## Expected Result

When the automatic vLLM preset selection fails, the error message should state the specific reason (e.g. that available GPU memory is below the recipe's minimum), so the user has an actionable path forward.

## Actual Result

```text
vLLM install failed: No automatic managed inference preset matched.
[non-interactive] Aborting: vLLM install failed. See errors above.

Onboarding did not finish. Resume from the step that failed with:
  nemoclaw onboard --resume --name {sandbox}
Completed steps are skipped; pass --fresh instead to start over.
[ERROR] Onboarding did not complete successfully.
```

The message gives no indication of the actual reason for the failure. Onboarding cannot complete on this hardware and the user has no way to diagnose or work around the problem from the CLI output alone.

## Logs

```text
nvidia@localhost:~$ curl -fsSL https://www.nvidia.com/nemoclaw.sh \
  | NEMOCLAW_INSTALL_TAG=v0.0.119 \
    NEMOCLAW_PROVIDER=install-vllm \
    NEMOCLAW_YES=1 \
    NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 \
    NEMOCLAW_NON_INTERACTIVE_SUDO_MODE=prompt \
    bash

[INFO]  Detected N1x. Skipping express prompt (NEMOCLAW_PROVIDER=install-vllm already set).

[1/3] Node.js
[INFO]  Node.js found: v22.23.2
[INFO]  Runtime OK: Node.js v22.23.2, npm 10.9.8

[2/3] NemoClaw CLI
[INFO]  Resolved install ref: v0.0.119
  Cloning NemoClaw source / Preparing OpenClaw package / Installing NemoClaw dependencies / Building NemoClaw CLI modules / Building NemoClaw plugin / Linking NemoClaw CLI / Installing OpenShell CLI - all OK
[INFO]  Verified: nemoclaw is available

[3/3] Onboarding
[non-interactive] Third-party software notice accepted via --yes-i-accept-third-party-software.
[INFO]  Running nemoclaw onboard...
  [non-interactive] Agent: OpenClaw

  NemoClaw Onboarding
  (non-interactive mode)
  ===================

  [1/8] Preflight checks
  Docker daemon: server 29.2.1
  Docker CDI GPU support detected (/etc/cdi/nvidia.json, /var/run/cdi/nvidia.yaml)
  Docker can start bridge containers
  Docker container DNS resolution works
  Container runtime: docker
  Container runtime resources: 18 vCPU / 22.1 GiB
  openshell CLI: openshell 0.0.106
  Port 8080 available (OpenShell gateway)
  NVIDIA GPU detected (NVIDIA RTX Spark N1X (5120-core Blackwell RTX GPU), 22631 MB)
  Sandbox GPU: enabled (auto)
  Memory OK: 22631 MB RAM + 16383 MB swap
  NVIDIA GPU detected; enabling OpenShell GPU passthrough. Use --no-gpu to opt out.

  [2/8] Starting OpenShell gateway
  Starting OpenShell Docker-driver gateway via managed service...
  OpenShell gateway managed service is healthy

  [3/8] Configuring inference provider
  [non-interactive] Provider: install-vllm
  vLLM install failed: No automatic managed inference preset matched.
  [non-interactive] Aborting: vLLM install failed. See errors above.

  Onboarding did not finish. Resume from the step that failed with:
    nemoclaw onboard --resume --name {sandbox}
  Completed steps are skipped; pass --fresh instead to start over.
[ERROR] Onboarding did not complete successfully.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8ee4e37e3be5e8b1ca884c263b9b3598f2e559c1`.  There
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
{"case_id": "NVIDIA_NemoClaw__11040__8ee4e37",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
