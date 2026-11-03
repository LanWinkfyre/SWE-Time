# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Onboard] Express install selects smaller Ollama model despite a larger installed model

> [!WARNING]
> **Regression** — closed as fixed in #10103 (expected in v0.0.119), still broken in v0.0.119.

## Description
On RTX Spark N1X running WSL2, NemoClaw Express install selects different local Ollama models as installed models are removed. When `qwen3.6:35b` remains installed, Express install selects smaller models instead of selecting the model expected for the device GPU capacity.

This was originally reproduced on v0.0.114, closed via #10103 as fixed in v0.0.119, and then reproduced again on v0.0.119: Express install selected `qwen3.5:9b` instead of `qwen3.6:35b`.

Platform scope: Reproduced on WSL2 only; other platforms not tested.

Regression: Yes — still broken in v0.0.119 after #10103 was closed as fixed. Last-good version not established.

OpenShell issue: No.

## Environment
```text
Device:        RTX Spark N1X
OS:            Windows build 28000.2787 with WSL release 2.6.3
Architecture:  arm64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.7.2
OpenShell CLI: openshell 0.0.106
NemoClaw:      originally v0.0.114; still reproduces on v0.0.119
OpenClaw:      2026.7.1
```

## Steps to Reproduce
1. On WSL2, make these Ollama models available: `llama3.2:latest`, `qwen3.6:latest`, `qwen3.5:9b`, and `qwen3.6:35b`.
2. Run:

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash
```

3. Accept the third-party software notice and confirm Express install. Observe that `llama3.2:latest` is selected.
4. Remove `llama3.2:latest` and repeat steps 2-3. Observe that `qwen3.6:latest` is selected.
5. Remove `qwen3.6:latest` and repeat steps 2-3. Observe that `qwen3.5:9b` is selected while `qwen3.6:35b` remains installed.

On the v0.0.119 retest, only `qwen3.5:9b` and `qwen3.6:35b` were installed, and Express install still selected `qwen3.5:9b`.

## Expected Result
Express install selects the largest installed Ollama model compatible with the device GPU capacity. For this device, it should select `qwen3.6:35b` when that model is installed.

## Actual Result
With all four models available, Express install selects `llama3.2:latest`. After removing it, it selects `qwen3.6:latest`. After removing that model, it selects `qwen3.5:9b` instead of `qwen3.6:35b`.

On v0.0.119 with `qwen3.5:9b` and `qwen3.6:35b` installed, Express install still selected `qwen3.5:9b`.

## Logs
```text
NAME           SIZE
qwen3.5:9b     6.6 GB
qwen3.6:35b    22 GB

Loading Ollama model: qwen3.5:9b
Model:         qwen3.5:9b
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `efd56a372999acc9d97936e9b30b2164743255a5`.  There
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
{"case_id": "NVIDIA_NemoClaw__10954__efd56a3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
