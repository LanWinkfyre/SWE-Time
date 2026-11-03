# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(ollama): recovery assertion expects a breadcrumb product does not emit

## Investigation Summary

- The [GPU Ollama target](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568885989) completes the Hermes path and appears to recover OpenClaw, but fails a stdout assertion.
- The same missing breadcrumb repeats on [later main](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678909412).
- The expected literal `Checking Ollama model readiness after daemon restart` exists in the test but not in product source at the candidate revision.
- This is a stale observability contract, not evidence that Ollama inference failed.

## Description

The GPU qualification target keys recovery success to a log message the product no longer emits.

Expected: the test asserts a stable recovery outcome—ready route plus a successful turn—or the product emits a deliberately supported machine-readable event.

Actual: functional recovery proceeds but the target fails on a stale string.

## Reproduction Steps

1. Run the GPU Ollama OpenClaw/Hermes target.
2. Allow daemon restart and recovery to complete.
3. Observe the missing stdout breadcrumb assertion.

## Environment

- GitHub Actions GPU Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Acceptance Criteria

- Replace the string assertion with a stable readiness/turn assertion, or restore a supported structured event.
- Preserve coverage that the daemon was restarted rather than skipped.
- Both OpenClaw and Hermes GPU turns pass.

## Candidate Fix

- [PR #11013 — test(e2e): assert Ollama recovery outcomes](https://github.com/NVIDIA/NemoClaw/pull/11013), authored by @apurvvkumaria.
- Status at linkage: open and ready for review.
- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) fails on the same stale Checking Ollama model readiness after daemon restart string.
- #11013 removes only the stale progress-sentence assertion while retaining daemon restart, unloaded-model state, successful agent turn, and reloaded-model state.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fa08360a2a873d3e3a797c67277fde6e93887513`.  There
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
{"case_id": "NVIDIA_NemoClaw__10973__fa08360",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
