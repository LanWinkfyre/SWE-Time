# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Linux][Sandbox] status exits nonzero with inference.local 503 while sandbox remains Phase Ready

## Description

A sandbox-scoped status command exits nonzero because the managed inference route returns HTTP 503, while the same status output still reports the sandbox as Phase Ready, route reachability as reachable, and the upstream provider as healthy. Automation and users therefore receive contradictory readiness signals for an otherwise Ready sandbox.

Product contract: a sandbox that is reported as Phase Ready and usable should provide a successful sandbox-scoped status result, or it should report a non-ready/degraded state consistently when the local managed inference route is unavailable. Snapshot restore and lifecycle flows also require the destination sandbox to remain usable after Ready is reported.

Platform scope: Reproduced on DGX Spark, Jetson Thor, Ubuntu 26.04 GPU, and WSL2 x86 release-validation runners. Ubuntu 22.04, Ubuntu 24.04, macOS, WSL2 ARM, and DGX Station did not provide a clean verdict for this exact failure in the same validation pass.

Regression: Unknown — earlier versions were not checked with this exact restore/status contract.

OpenShell issue: No — the failing surface is NemoClaw sandbox status and managed inference route health reporting.

Exclusions: the representative failures reached product behavior. They are not missing credential failures, not setup-hook failures, not runner preflight failures, and not external provider outages because the same output reports the upstream provider as healthy and route reachability as reachable.

## Environment

- Device: Release-validation Linux, DGX Spark, Jetson Thor, Ubuntu GPU, and WSL2 x86 runners
- OS: Supported Linux and WSL2 Ubuntu release-validation environments
- Architecture: x86_64 and aarch64
- Node.js: v22.23.x from CI snapshots
- npm: 10.9.x from CI snapshots
- Docker: Docker Engine 29.x on Linux and Docker Desktop or WSL2 Docker backend where applicable
- OpenShell CLI: openshell 0.0.106
- NemoClaw: nemoclaw v0.0.116
- OpenClaw: OpenClaw runtime available in the Ready sandbox; exact version was not consistently captured in the logs

## Steps to Reproduce

1. Install NemoClaw v0.0.116 on a supported Linux or WSL2 host with Docker available.
2. Onboard an OpenClaw sandbox with a valid managed inference provider and wait until the sandbox reports Phase Ready.
3. Exercise a snapshot restore or sandbox lifecycle path that checks sandbox-scoped status immediately after Ready is reported.
4. Run the sandbox-scoped status command, for example: `nemoclaw sandbox-name status`.
5. Inspect the command exit code and readiness details in the output.

## Expected Result

The sandbox-scoped status command exits 0 for a Ready and usable sandbox. If the local managed inference route is unavailable, status reports a consistent degraded or non-ready state instead of returning a failure while still presenting the sandbox as Phase Ready with reachable route and healthy upstream provider.

## Actual Result

The sandbox-scoped status command exits nonzero. The output reports the sandbox as Phase Ready, reports route reachability as reachable, and reports the upstream provider as healthy, but also reports the managed inference route as unhealthy because a sandbox inference invocation probe returned HTTP 503.

## Logs

Representative sanitized release-validation excerpt:

```text
AssertionError: destination status failed:
Sandbox-scoped status for destination sandbox:
  Inference: unhealthy (https://inference.local/v1/models)
    Inference gateway did not serve an inference request: sandbox inference invocation probe returned HTTP 503.
  Inference route reachability: reachable (https://inference.local/v1/models)
  Inference upstream: healthy
  Phase: Ready
```

Additional representative source-sandbox status failures showed the same pattern: sandbox-scoped status exited nonzero, inference.local returned HTTP 503, route reachability was reachable, upstream provider was healthy, and Phase remained Ready.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f59e93ce0abd06c6ecf4d2930c183dfe90c5e495`.  There
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
{"case_id": "NVIDIA_NemoClaw__10709__f59e93c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
