# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
upgrade: legacy OpenClaw sandboxes are rejected as DCode prepared contexts

## Investigation Summary

- Four legacy upgrade targets fail on `3076188279c0ea657ec77aeeabebf1f82061eaaf`: [v0.0.55 x86](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568887274), [v0.0.55 ARM64](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568887291), [v0.0.74 x86](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568887328), and [v0.0.89 x86](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568887222).
- All four repeat on `eb3fa2e5097389d7dd8e2643552788ff16d8f14a`: [v0.0.55 x86](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907757), [v0.0.55 ARM64](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907077), [v0.0.74](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907162), and [v0.0.89](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907344).
- Each aborts after backing up and deleting the old sandbox with the same prepared-context error.
- The legacy prepared context lacks target metadata; the current code defaults that ambiguous context to DCode and rejects the identified OpenClaw sandbox.

## Description

Supported upgrades from four released versions cannot recreate an OpenClaw sandbox because the prepared rebuild context loses or never receives its agent target.

Expected: the upgrade carries the detected OpenClaw target through preparation and recreation.

Actual: the context is treated as DCode-only and is rejected after destructive upgrade work has begun.

## Reproduction Steps

1. Create a sandbox from any of v0.0.55, v0.0.74, or v0.0.89 using the linked E2E fixture.
2. Run the candidate upgrade workflow.
3. Observe failure during sandbox recreation.

## Environment

- GitHub Actions Docker, x86-64 and ARM64
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Debug Output

```text
Sandbox recreate error: A prepared DCode build context cannot be used for this sandbox target.
```

## Acceptance Criteria

- Prepared contexts always preserve an explicit rebuild target.
- Legacy context compatibility selects the detected sandbox agent instead of assuming DCode.
- All four upgrade targets pass together, including state-preservation assertions.


## Candidate Fix

- [PR #10996 — fix(sandbox): repair Shields removal regressions](https://github.com/NVIDIA/NemoClaw/pull/10996), authored by @ericksoa.
- Status after the latest main merge: open and changes requested. The branch includes current `main` but still must remove the superseded #10963 and unrelated messaging work.
- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) reproduces the prepared-DCode failure on v0.0.55 x86-64, v0.0.55 Arm64, v0.0.74, and v0.0.89.
- #10996 remains the intended owner for preserving the prepared rebuild argument and target contract. Keep this issue open until the reduced PR passes all four exact-head upgrade targets.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `94bb868ea0f3e98533b06196def74b7559a1d1d4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10964__94bb868",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
