# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Onboard] managed llama.cpp private bridge probe fails on Docker Desktop WSL2 due to --network host namespace isolation

## Description

On NemoClaw v0.0.122 running under Docker Desktop WSL2 (ARM64, N1X), the managed
llama.cpp onboarding fails at step [3/8] with "Docker llama.cpp private loopback
bridge probe failed (exit 7)". The probe runs a curl container with `--network host`
to reach `127.0.0.1:{hostPort}/health`, but Docker Desktop's `--network host` shares
the Docker VM's network namespace — not the WSL2 distro's — so curl cannot reach
the private bridge process listening on WSL2's loopback.

Platform scope: Reproduced on WSL2 ARM64 (N1X) only; other platforms not tested.
Docker Desktop WSL2 is the affected configuration; native Linux Docker (where
`--network host` truly shares the host namespace) is expected to work.

Regression: Unknown — earlier versions not tested (first managed llama.cpp attempt
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
2. Ensure Docker Desktop has sufficient memory (56 GB via `.wslconfig`) and GPU access
3. Run:
   ```bash
   DOCKER_CONFIG=$(mktemp -d) nemoclaw onboard --fresh --name my-assistant --non-interactive
   ```
4. Observe step [1/8] Preflight checks pass (GPU detected, Docker GPU proof passes)
5. Observe step [2/8] Gateway reuse succeeds
6. Observe step [3/8] fails with: "Managed llama.cpp install failed: Docker llama.cpp private loopback bridge probe failed (exit 7)."

## Expected Result

The private loopback bridge probe should succeed, allowing managed llama.cpp
onboarding to proceed past step [3/8]. The probe should account for Docker
Desktop WSL2's network topology where `--network host` does not share the WSL2
distro's loopback interface.

## Actual Result

Step [3/8] fails:

```text
[non-interactive] Provider: install-llama-cpp
Verifying the exact llama.cpp GGUF in the shared Hugging Face cache
Managed llama.cpp install failed: Docker llama.cpp private loopback bridge probe failed (exit 7).
[non-interactive] Aborting: Docker llama.cpp private loopback bridge probe failed (exit 7).
```

Exit code 7 is curl's "Failed to connect to host." The probe runs:

```bash
docker run --rm --pull=never --network host --entrypoint curl {image} http://127.0.0.1:{port}/health
```

With Docker Desktop, `--network host` gives the container the Docker VM's
network namespace, not WSL2's. The private bridge Node.js process listens
on WSL2's `127.0.0.1`, which is unreachable from the Docker VM's `127.0.0.1`.

Note: The preflight correctly detects "Docker Desktop WSL" and uses the
"--gpus compatibility path instead of CDI spec validation" — but the
private bridge probe does not adapt its network strategy for Docker Desktop.

## Logs

```text
Full onboard output (second attempt, after fixing .wslconfig/zstd/HF-cache issues):

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
  Port 8080 already owned by healthy NemoClaw runtime (OpenShell gateway)
  NVIDIA GPU detected (NVIDIA RTX Spark N1X (6144-core Blackwell RTX GPU), 63936 MB)

  [2/8] Starting OpenShell gateway
  [reuse] Skipping gateway (running)

  [3/8] Configuring inference provider
  [non-interactive] Provider: install-llama-cpp
  Verifying the exact llama.cpp GGUF in the shared Hugging Face cache
  Managed llama.cpp install failed: Docker llama.cpp private loopback bridge probe failed (exit 7).
  [non-interactive] Aborting: Docker llama.cpp private loopback bridge probe failed (exit 7).

Verification that --network host cannot reach WSL2 loopback:
  A Python HTTP server started on WSL2 127.0.0.1:19876 was unreachable from
  docker run --network host (curl returned 000), while host.docker.internal:8080
  from the same --network host container returned 404 (reachable). This confirms
  Docker Desktop VM's loopback is isolated from WSL2's loopback.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `56f4b626d333e76b7831fe0ff5d3a08b60a62ddc`.  There
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
{"case_id": "NVIDIA_NemoClaw__11436__56f4b62",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
