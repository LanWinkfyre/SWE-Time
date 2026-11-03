# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
DGX Station Express GPU handoff fails before the configured readiness deadline

## Investigation Summary

- DGX Station Express onboarding proves CUDA and reaches `Ready` before the compatibility GPU final handoff.
- The final handoff removes the backup, issues `openshell sandbox start`, and fails while OpenShell still reports `Provisioning`.
- Docker still reports the transaction-owned replacement as running with health `starting`.
- PR #10339 introduced the OpenShell stop and start sequence. OpenShell v0.0.106 uses a separate lifecycle timeout, which can expire before the NemoClaw 900-second handoff budget.
- The failed attempt leaves a verified-create checkpoint. The independent recovery journal also failed to persist, so same-name Express retries cannot proceed. The journal write cause is not present in the terminal error.

## Description

DGX Station Express onboarding fails during the Docker GPU compatibility handoff. The replacement passes the first managed readiness check and CUDA initialization. NemoClaw then stops the replacement through OpenShell, removes the previous container, and starts the replacement through OpenShell.

`openshell sandbox start` returns nonzero while the sandbox remains in the nonterminal `Provisioning` phase. The exact replacement container remains running. NemoClaw classifies the command result as a failed restart and stops before its final bounded readiness waiter runs.

Expected behavior: after the start request has a transport or readiness failure, NemoClaw must reconcile the effect. It may continue the existing final handoff waiter only while Docker proves the transaction-owned replacement is the sole running sandbox container and OpenShell reports a nonterminal phase. Missing, foreign, ambiguous, or terminal state must remain a failure.

The failed attempt also exposed a recovery gap. The registry retained `pendingCreateIdentity`, but `retained-sandbox-recovery.json` was not written. A later Express run selected the saved `my-assistant` name, created a new onboarding session, configured inference, and then failed because the old verified-create checkpoint belongs to another session. `--resume` and `--fresh` do not resolve this state.

## Reproduction Steps

1. On a DGX Station GB300, run `./install.sh` and select Express installation with local vLLM.
2. Accept the default `my-assistant` sandbox name and enable GPU passthrough.
3. Let onboarding use the Docker GPU compatibility path.
4. Observe that CUDA initialization succeeds and the replacement reaches the first managed `Ready` check.
5. During the final handoff, observe `Stopping the replacement through OpenShell` followed by `Starting the exact replacement through OpenShell`.
6. Observe onboarding fail without printing `Waiting for OpenShell to confirm the final replacement handoff`.
7. Confirm `openshell sandbox list` reports `Provisioning` at failure time and Docker reports the replacement as running with health `starting`.
8. Run `./install.sh` again.
9. Observe `Cannot replace sandbox my-assistant while its verified create checkpoint is incomplete` after inference configuration.

## Environment

- Hardware: DGX Station GB300
- Install mode: Express
- Agent: OpenClaw
- Inference: local vLLM
- Model: `nvidia/nemotron-3-ultra-550b-a55b`
- OpenShell: v0.0.106, as pinned by the tested NemoClaw source
- Gateway: `nemoclaw`, port 8080
- GPU route: Docker compatibility path
- OS, Node.js, Docker, and exact NemoClaw revision: not captured in the supplied terminal evidence

## Debug Output

The failure diagnostics reported:

```text
Managed startup passed Ready, but its final runtime handoff did not converge.
The previous container was removed at the final handoff commit point; automatic rollback is unavailable.
OpenShell supervisor did not reach Ready (last phase: Provisioning).
patched_container_status=running
patched_container_running=true
patched_container_exit_code=0
patched_container_health=starting
patched_create_option=persistent sandbox startup command
```

Persisted state after the failure contained:

```text
pendingRouteReservation=true
pendingCreateIdentity.state=verified-create
pendingCreateIdentity.route=native
```

Later inspection found no OpenShell sandbox, no matching Docker container, and no retained recovery journal. The retry failed with:

```text
Error: Cannot replace sandbox my-assistant while its verified create checkpoint is incomplete
```

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `814772eedd4c1f2fd7a8769a33c3032b30076811`.  There
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
{"case_id": "NVIDIA_NemoClaw__11096__814772e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
