# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
upgrade: v0.0.115 Shields sandbox cannot pass durable receipt migration

## Investigation Summary

- The [v0.0.115 Shields migration](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568887292) correctly detects the retired Shields posture, then fails the supported automatic upgrade.
- The same receipt mismatch repeats on [later main](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907569).
- Managed workload rebuild preflight rejects the released sandbox because its live qualification revision differs from its durable workload receipt.
- This migration was exposed by the Shields removal in [PR #10722](https://github.com/NVIDIA/NemoClaw/pull/10722).

## Description

A released v0.0.115 Shields sandbox is intentionally blocked from continuing unchanged, but the supported `upgrade-sandboxes --auto` recovery path also refuses it. Users are left without a successful supported migration.

Expected: the retirement gate directs the sandbox into a validated migration that rebuilds it on the candidate image while preserving state.

Actual: durable receipt parity prevents the required rebuild.

## Reproduction Steps

1. Create the v0.0.115 Shields fixture.
2. Run the candidate's automatic sandbox upgrade.
3. Observe preflight reject the live/durable qualification revision mismatch.

## Environment

- GitHub Actions Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Debug Output

```text
Managed workload rebuild preflight failed: the live qualification revision does not match the durable workload receipt.
```

## Acceptance Criteria

- Define and implement the supported trust transition for a released Shields-era receipt.
- Preserve user state while preventing arbitrary receipt bypass.
- The v0.0.115 migration target passes end to end.


## Candidate Fix

- [PR #10996 — fix(sandbox): repair Shields removal regressions](https://github.com/NVIDIA/NemoClaw/pull/10996), authored by @ericksoa.
- Status after the latest main merge: open and changes requested. The branch includes current `main` but still must remove the superseded #10963 and unrelated messaging work.
- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) reproduces the v0.0.115 Shields migration refusal after backup and deletion.
- #10996 remains the intended owner for the candidate managed-image revision and durable source-receipt transition. Keep this issue open until the reduced PR passes the exact-head Shields migration target.
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
{"case_id": "NVIDIA_NemoClaw__10970__94bb868",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
