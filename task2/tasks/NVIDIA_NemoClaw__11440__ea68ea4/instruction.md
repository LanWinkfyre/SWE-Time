# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Onboard] Express install fails with "Managed llama.cpp requires a selected sandbox name"

## Description

On NemoClaw v0.0.122 running under Docker Desktop WSL2 (ARM64, N1X), the
express install fails at step [3/8] "Configuring inference provider" with
"Managed llama.cpp requires a selected sandbox name." The express install
preamble correctly shows "Sandbox name: my-assistant" but the non-interactive
onboard path does not forward this sandbox name to the managed llama.cpp
provider selection logic.

Platform scope: Reproduced on WSL2 ARM64 (N1X) only; other platforms not tested.
Regression: Unknown — earlier versions not tested (first express install attempt
on this platform).
OpenShell issue: No

## Environment

```text
Device:        NVIDIA RTX Spark N1X (WoA laptop)
OS:            Ubuntu 24.04.4 LTS under WSL2 (WSL kernel 6.6.87-microsoft-standard-WSL2)
Architecture:  aarch64 (ARM64)
GPU:           NVIDIA RTX Spark N1X (6144-core Blackwell RTX GPU), 63936 MiB, driver 616.79
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker Desktop 4.90.0 (238679), Engine 29.7.2
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.122
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. Install NemoClaw v0.0.122 on an N1X WSL2 (Ubuntu 24.04) system with Docker Desktop
2. Run the express install (default non-interactive path):
   ```bash
   NEMOCLAW_INSTALL_VERSION=0.0.122 bash -c "$(curl -fsSL https://raw.githubusercontent.com/NVIDIA/NemoClaw/main/install.sh)"
   ```
3. Observe the express preamble showing correct config:
   `Sandbox name: my-assistant` / `Inference: Managed llama.cpp`
4. Observe step [3/8] "Configuring inference provider" fails immediately

## Expected Result

The express install non-interactive path should forward the sandbox name
("my-assistant") to the managed llama.cpp provider selection at step [3/8],
allowing onboarding to proceed.

## Actual Result

Step [3/8] fails:

```text
[3/8] Configuring inference provider
[non-interactive] Provider: install-llama-cpp
Managed llama.cpp requires a selected sandbox name.
[non-interactive] Aborting: Managed llama.cpp requires a selected sandbox name.
```

The express installer sets "Sandbox name: my-assistant" in its preamble but
the managed llama.cpp provider at step [3/8] does not receive this value.
The workaround is to run onboard manually:
`nemoclaw onboard --fresh --name my-assistant --non-interactive`
which correctly passes the sandbox name (but then hits a separate bridge
probe issue on Docker Desktop WSL2, tracked separately).

## Logs

```text
Full express install output (fresh install on clean WSL2 distro):

  NemoClaw Express Install
  ========================
  Version: 0.0.122
  Sandbox name: my-assistant
  Inference: Managed llama.cpp

  [1/3] Installing NemoClaw
  ...
  [2/3] Installing OpenShell
  ...
  [3/3] Onboarding
  [1/8] Preflight checks
  Running bounded Docker GPU proof for NVIDIA RTX Spark N1X (6144-core Blackwell RTX GPU)...
  Docker GPU capacity proof: 23299 MiB available of 63936 MiB.
  Docker daemon: server 29.7.2
  Docker Desktop WSL detected; using Docker --gpus compatibility path instead of CDI spec validation.
  Docker can start bridge containers
  Container runtime: docker-desktop
  Running under WSL
  Container runtime resources: 16 vCPU / 54.8 GiB
  openshell CLI: openshell 0.0.106
  NVIDIA GPU detected (NVIDIA RTX Spark N1X (6144-core Blackwell RTX GPU), 63936 MB)

  [2/8] Starting OpenShell gateway
  ...

  [3/8] Configuring inference provider
  [non-interactive] Provider: install-llama-cpp
  Managed llama.cpp requires a selected sandbox name.
  [non-interactive] Aborting: Managed llama.cpp requires a selected sandbox name.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ea68ea444a9f7e27455961ca0412258d47dca489`.  There
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
{"case_id": "NVIDIA_NemoClaw__11440__ea68ea4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
