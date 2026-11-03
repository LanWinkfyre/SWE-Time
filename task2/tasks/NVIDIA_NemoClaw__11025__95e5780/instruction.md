# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Station][CLI&UX] Intentional stop is reported as a failure - status prints "Failure layer: sandbox_container_stopped" and Phase: Provisioning instead of Stopped

## Description

A clean, workspace-preserving stop leaves the sandbox reported as a failure rather than as stopped. `nemoclaw <sandbox> stop` succeeds and prints that workspace state is preserved, but the very next `nemoclaw <sandbox> status` prints a `Failure layer` line and reports `Phase: Provisioning`. A user who intentionally stopped a sandbox is shown failure wording and a transitional phase for a state they deliberately created.

The status output does also contain the plain sentence `Sandbox '<sandbox>' is stopped.`, so the information is present; the problem is that the leading, prominent lines classify an intentional stop as a failure and as Provisioning rather than as Stopped.

**Platform scope:** Reproduced on DGX Station aarch64 and on DGX Spark aarch64; observed with both NVIDIA Endpoints and Local Ollama providers.
**Regression:** Unknown — earlier versions not tested for this exact wording.

## Environment

```text
Device:        DGX Station (aarch64)
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.2.1
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. Onboard an OpenClaw sandbox and confirm it reports `Phase: Ready`.
2. Run `nemoclaw <sandbox> stop`.
3. Run `nemoclaw <sandbox> status`.

## Expected Result

After an intentional, workspace-preserving stop, status reports the sandbox as **Stopped**. No failure-layer classification is printed for a state the user asked for.

## Actual Result

```text
nemoclaw <sandbox> stop
  Sandbox '<sandbox>' stopped. Workspace state is preserved.
  Start it again with 'nemoclaw <sandbox> start'.
exit code 0

nemoclaw <sandbox> status
  Failure layer: sandbox_container_stopped — sandbox container exists but is not running.
  Phase: Provisioning
  Sandbox '<sandbox>' is stopped.
```

## Logs

```text
Reproduced three times across two machines:
  DGX Spark   — stop exit 0, then status prints Failure layer: sandbox_container_stopped and Phase: Provisioning
  DGX Station — same output with an NVIDIA Endpoints sandbox
  DGX Spark   — same output with a Local Ollama sandbox
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95e578095c6cf99d400f25768e7f862c7b6ccd49`.  There
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
{"case_id": "NVIDIA_NemoClaw__11025__95e5780",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
