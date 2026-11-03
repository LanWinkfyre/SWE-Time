# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Install] nemoclaw uninstall fails to remove gateway registration when Docker is unavailable, leaving host in a permanently broken state

## Description

On a Windows WSL2 host with no working Docker runtime (Docker Desktop WSL integration not enabled for this distro), `nemoclaw uninstall` fails at the OpenShell gateway removal step across all three documented invocation forms (plain, `--all-gateway-ports`, `--yes`), each time exiting 1 with only "openshell gateway remove failed (exit 1)" and no recovery path. A fresh reinstall on the same host confirms `nemoclaw onboard` correctly detects and reports the same missing-Docker precondition with actionable guidance, but `uninstall` does not have equivalent handling.

**Platform scope:** Reproduced on Windows WSL2 (Ubuntu distro) only; other platforms not tested.
**Regression:** Unknown — earlier versions not tested on this host.
**OpenShell issue:** No

## Environment

```text
Device:        Windows WSL2 host (Ubuntu distro), Docker Desktop WSL integration not enabled
OS:            Windows WSL2 / Ubuntu (exact Ubuntu version not captured)
Architecture:  Not captured
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Not installed / not available (docker: command not found)
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.122
OpenClaw:      N/A — current host preflight blocks onboarding entirely due to missing Docker; the pre-existing gateway registration predates this session and its OpenClaw version could not be verified
```

## Steps to Reproduce

1. On a Windows WSL2 host where Docker Desktop WSL integration is not enabled (`docker` command unavailable), with an existing NemoClaw gateway registration from a prior onboarding attempt, run:
   ```bash
   nemoclaw uninstall
   ```
2. Confirm the prompt with `y`. Observe it stops at step `[2/6] OpenShell resources` with:
   ```text
   Could not remove gateway registration 'nemoclaw': openshell gateway remove failed (exit 1).
   ```
3. Retry with `nemoclaw uninstall --all-gateway-ports` — same failure.
4. Retry with `nemoclaw uninstall --yes` — same failure.
5. Confirm no Docker runtime is present:
   ```bash
   docker ps
   # Command 'docker' not found, but can be installed with: sudo snap install docker
   ```
6. Reinstall fresh on the same host (`curl | bash`) and run onboarding — preflight correctly detects and reports the missing-Docker precondition with admission finding IDs `host.platform.wsl_runtime_unavailable`, `host.docker.unavailable`, `host.gpu.container_toolkit_missing`, and actionable remediation steps (enable Docker Desktop WSL integration, run `wsl --shutdown`, retry). Onboarding is cleanly blocked rather than left in a broken state.

## Expected Result

When the OpenShell/Docker gateway backend is unavailable, `nemoclaw uninstall` should either still remove its own local gateway registration and state, or clearly report that Docker/OpenShell is unreachable with a supported recovery path — similar to how `nemoclaw onboard` on the same host correctly detects and reports the missing-Docker precondition with actionable guidance, instead of exiting 1 mid-uninstall with only "openshell gateway remove failed (exit 1)" and no next step.

## Actual Result

All three uninstall invocations produced the identical failure:

```text
[2/6] OpenShell resources
OpenShell sandboxes already removed or unreachable
Provider 'nvidia-nim' already removed or unreachable
Provider 'vllm-local' already removed or unreachable
Provider 'ollama-local' already removed or unreachable
Provider 'nvidia-ncp' already removed or unreachable
Provider 'nim-local' already removed or unreachable
Could not remove gateway registration 'nemoclaw': openshell gateway remove failed (exit 1).
Uninstall completed with errors. Some state may remain on disk; see warnings above.
```

None of the three variants (plain, `--all-gateway-ports`, `--yes`) succeeded, and no recovery path was offered. The only way to reach a clean state was manually deleting the NemoClaw state directory by hand, which is outside the documented uninstall flow.

## Logs

```text
$ nemoclaw version
nemoclaw v0.0.122

$ nemoclaw uninstall
  Running local uninstall script: {home}/.nemoclaw/source/uninstall.sh
NemoClaw Uninstaller
This will remove all NemoClaw resources.
Proceed? [y/N]
y
[1/6] Stopping services
Disabled nemoclaw-openshell-gateway.service
Removed {home}/.config/systemd/user/nemoclaw-openshell-gateway.service
No orphaned openshell processes found
No host openshell-gateway processes found
[2/6] OpenShell resources
OpenShell sandboxes already removed or unreachable
Provider 'nvidia-nim' already removed or unreachable
Provider 'vllm-local' already removed or unreachable
Provider 'ollama-local' already removed or unreachable
Provider 'nvidia-ncp' already removed or unreachable
Provider 'nim-local' already removed or unreachable
Could not remove gateway registration 'nemoclaw': openshell gateway remove failed (exit 1).
Uninstall completed with errors. Some state may remain on disk; see warnings above.

$ nemoclaw uninstall --all-gateway-ports
(same prompt and identical failure at [2/6])

$ nemoclaw uninstall --yes
(same identical failure at [2/6], no prompt)

$ docker ps
Command 'docker' not found, but can be installed with:
sudo snap install docker

--- Fresh reinstall on the same host, confirming Docker is genuinely unavailable ---

$ curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.122 bash
...
[3/3] Onboarding
Running under WSL
[WARN]  Host preflight found issues that will prevent onboarding right now.
  Admission finding IDs: host.platform.wsl_runtime_unavailable, host.docker.unavailable, host.gpu.container_toolkit_missing
  Admission capability IDs: host.docker.runtime_supported, host.docker.storage_compatible, host.docker.storage_remediation_available
  - Enable Docker Desktop WSL integration: Docker is not available inside this WSL distro. When using Docker Desktop on Windows, WSL integration must be enabled for the Ubuntu distro before NemoClaw can create a gateway or sandbox.
    Open Docker Desktop, Settings, Resources, WSL integration.
    Enable integration for this Ubuntu distro, apply the change, then run wsl --shutdown from Windows PowerShell.
    Reopen Ubuntu, verify docker info, then rerun nemoclaw onboard.
  - WSL has no available Docker runtime.
  - Docker is not installed.
  - NVIDIA Container Toolkit is missing.
[ERROR] Skipping onboarding until the host prerequisites above are fixed.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c85070d995da12107932d103f03d00e7391ee660`.  There
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
{"case_id": "NVIDIA_NemoClaw__11438__c85070d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
