# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Onboard] vLLM model selection during Deep Agents onboarding loops forever, fails on a DGX Spark readiness check

## Description

LangChain Deep Agents onboarding on N1x, with the vLLM provider explicitly selected, fails every time at model selection with a DGX-Spark-specific readiness error on non-DGX-Spark hardware, then re-prompts the same model choice indefinitely with no way to exit except killing the process.

Platform scope: Reproduced on N1x Linux only; other platforms not tested.
Regression: Unknown — earlier versions not tested.
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
OpenClaw:      N/A (onboard not completed — this path uses LangChain Deep Agents Code, and never reached agent runtime setup)
```

## Steps to Reproduce

1. On N1x Linux, decline the Deferred N1x Express preview when prompted, then run:
   ```bash
   export NEMOCLAW_PROVIDER=install-vllm
   ```
2. Run:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash
   ```
3. At "Select your agent:", choose `3) LangChain Deep Agents Code`
4. Onboarding proceeds through preflight (all checks pass) and reaches "[3/8] Configuring inference provider", Provider: install-vllm
5. At "Choose model [1]:", accept the default (`1`, Qwen3.6 35B-A3B NVFP4)

## Expected Result

The vLLM model install either succeeds, or fails once with a clear, actionable error message, leaving the user able to retry, choose a different model or provider, or exit onboarding cleanly.

## Actual Result

```text
vLLM install failed: Readiness requirement host.platform.dgx_spark did not match.
```

This message is printed on N1x hardware, which is not a DGX Spark. The model-selection prompt then re-appears and repeats the identical failure indefinitely, with no exit path other than killing the process (Ctrl+C). Onboarding never completes.

## Logs

```text
  Select your agent:
    1) OpenClaw
    2) Hermes Agent
    3) LangChain Deep Agents Code

  Choose [1]: 3

  NemoDeepAgents Onboarding
  ===================

  [1/8] Preflight checks
  Docker daemon: server 29.2.1
  Docker CDI GPU support detected
  Container runtime resources: 18 vCPU / 22.1 GiB
  openshell CLI: openshell 0.0.106
  Port 8080 available
  NVIDIA GPU detected (NVIDIA RTX Spark N1X (5120-core Blackwell RTX GPU))
  Sandbox GPU: enabled (auto)

  [2/8] Starting OpenShell gateway
  OpenShell gateway managed service is healthy

  [3/8] Configuring inference provider
  [non-interactive] Provider: install-vllm

  vLLM models for N1x:
    1) Qwen3.6 35B-A3B NVFP4 (recommended, default)
       nvidia/Qwen3.6-35B-A3B-NVFP4

  Choose model [1]: 1
  vLLM install failed: Readiness requirement host.platform.dgx_spark did not match.
  [non-interactive] Provider: install-vllm

  vLLM models for N1x:
    1) Qwen3.6 35B-A3B NVFP4 (recommended, default)
       nvidia/Qwen3.6-35B-A3B-NVFP4

  Choose model [1]: 1
  vLLM install failed: Readiness requirement host.platform.dgx_spark did not match.
  [non-interactive] Provider: install-vllm

  vLLM models for N1x:
    1) Qwen3.6 35B-A3B NVFP4 (recommended, default)
       nvidia/Qwen3.6-35B-A3B-NVFP4

  Choose model [1]: 1
  vLLM install failed: Readiness requirement host.platform.dgx_spark did not match.
  [non-interactive] Provider: install-vllm
  ... repeats indefinitely, same prompt, same failure, no exit path
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `afb2342666e0fa6b2dbaf23f1e194283b4787363`.  There
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
{"case_id": "NVIDIA_NemoClaw__11037__afb2342",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
