# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(onboard): repaired sandbox loses canonical CLI pairing

## Investigation Summary

- The exact-candidate [PR #11071 E2E run](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) tested commit `0ddc3ea52efe8a5d63099b92f43cbe0a43c88a01`.
- [Onboarding repair](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750616) created the initial sandbox, removed the recorded sandbox, and entered resume repair.
- The replacement reached gateway selection but then failed because its canonical OpenClaw CLI device pairing did not appear.
- Closed issue #10014 covered a related non-interactive pairing-finalization failure. Treat this as a possible regression, not as proof that the old root cause returned.

## Description

Resume repair can recreate a missing sandbox, but onboarding does not observe the canonical CLI pairing for the replacement. The repair path exits before it can verify conflicting resume input.

Expected: the recreated sandbox establishes or restores the canonical CLI pairing and resume completes.

Actual: onboarding reports that the pairing did not appear and exits 1.

## Acceptance Criteria

- Capture the pairing creation, lookup, and timeout evidence for the replacement sandbox identity.
- Determine whether the pairing is missing, late, or recorded under the retired sandbox identity.
- Preserve the existing non-interactive pairing boundary.
- Complete the missing-sandbox repair and conflicting-resume assertions on the same exact candidate.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fa7ad67666ba0b60ca3ebdaf9c610fd04f4083e1`.  There
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
{"case_id": "NVIDIA_NemoClaw__11085__fa7ad67",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
