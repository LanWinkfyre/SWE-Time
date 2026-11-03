# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Onboard][Regression] Express install fails at registry publication with "Deferred N1x preview acceptance failed closed validation"

## Description

On NemoClaw v0.0.122 on N1x Linux (native, not WSL2), the express install
completes vLLM installation and sandbox creation successfully (Phase: Ready,
GPU proofs pass), but fails at the final sandbox registry publication step
with "Sandbox Deferred N1x preview acceptance failed closed validation."

Root cause: `isDeferredN1xManagedVllmAcceptanceRoute()` requires
`endpointUrl === null`, but after managed vLLM installs successfully, the
inference selection sets `endpointUrl` to the vLLM endpoint. These two
requirements are mutually exclusive — managed vLLM cannot both be running
(endpointUrl set) and pass the N1x acceptance check (endpointUrl null).

> [!WARNING]
> **Regression** — N1x express install worked in v0.0.119; broken in v0.0.122 by the `isDeferredN1xManagedVllmAcceptanceRoute()` closed validation added in PR #11136.

Platform scope: Reproduced on N1x Linux (native) only; other platforms not tested.
OpenShell issue: No

## Environment

```text
Device:        N1x Linux Laptop (NVIDIA JMJWOA-Generic-GPU)
OS:            Linux 7.0.0-1015-nvidia aarch64
Architecture:  aarch64
GPU:           NVIDIA JMJWOA-Generic-GPU, driver 615.69
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker Engine (CDI enabled, nvidia.com/gpu spec present)
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.122
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. Install NemoClaw v0.0.122 on an N1x Linux (native) system:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.122 bash
   ```
2. Accept the Deferred N1x preview prompt ("Y")
3. Wait for vLLM image pull, model download, and container startup (~7 min)
4. Observe vLLM becomes ready ("vLLM is serving on :8000")
5. Observe sandbox creation succeeds (GPU proofs pass, Phase: Ready)
6. Observe final error: "Sandbox Deferred N1x preview acceptance failed closed validation."

## Expected Result

The N1x Deferred preview acceptance validation should succeed when managed
vLLM is installed and running, allowing the sandbox registry publication to
complete and the express install to finish.

## Actual Result

Express install fails at the very end after everything else succeeds:

```text
Create-attempt label: ai.nvidia.nemoclaw.create-attempt=7ec612c6...
Sandbox 'my-assistant' was retained after registry publication failed.
Error: Sandbox Deferred N1x preview acceptance failed closed validation.
[ERROR] Onboarding did not complete successfully.
```

Post-mortem state:
- vLLM container (nemoclaw-vllm): running, serving on localhost:8000
- OpenShell sandbox (my-assistant): Phase=Ready, GPU proofs passed
- NemoClaw registry: sandbox marked as incomplete with `pendingRouteReservation=true`
- `nemoclaw my-assistant`: "still being created by onboarding" (blocked)
- `nemoclaw my-assistant destroy`: blocked by retained-sandbox-recovery

The validation function `isDeferredN1xManagedVllmAcceptanceRoute()` checks:
- `route.endpointUrl === null` — **FAILS**: actual value is the vLLM endpoint
- `route.openshellDriver === "docker"` — status shows "unknown"

The `sandboxes.json` confirms endpointUrl is set after vLLM setup:
```
endpointUrl: "http://host.openshell.internal:8000/v1"
endpointSource: null
```

This creates a deadlock: managed vLLM must be running for the install to
proceed, but a running vLLM means endpointUrl is non-null, which the
acceptance validation rejects.

## Logs

```text
[3/8] Configuring inference provider
[non-interactive] Provider: install-vllm
vLLM (N1x):
  Image: nvcr.io/nvidia/vllm (pinned by digest)
  Model: nvidia/Qwen3.6-35B-A3B-NVFP4
...
vLLM is serving on :8000
vLLM ready on localhost:8000
Detected model: nvidia/Qwen3.6-35B-A3B-NVFP4
Responses API available
Using vLLM max_model_len: 32768 tokens

[6/8] Creating sandbox
Creating sandbox 'my-assistant'...
Building sandbox image...
Waiting for sandbox to become ready...
GPU proof passed: nvidia-smi when available
GPU proof passed: cuInit(0) via libcuda.so.1
Sandbox CUDA usability proven (cuInit succeeded).

Create-attempt label: ai.nvidia.nemoclaw.create-attempt=7ec612c6...
Sandbox 'my-assistant' was retained after registry publication failed.
Error: Sandbox Deferred N1x preview acceptance failed closed validation.
[ERROR] Onboarding did not complete successfully.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bf6e7bb624dcd9b37a62543a0b0bd912d017d5a7`.  There
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
{"case_id": "NVIDIA_NemoClaw__11510__bf6e7bb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
