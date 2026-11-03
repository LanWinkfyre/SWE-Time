# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
test(e2e): keep OpenClaw plugin EXDEV coverage at live boundaries

## Problem

The rewrite in #10517 reduced `test/e2e/live/openclaw-plugin-runtime-exdev.test.ts`, but later repairs and product changes exposed remaining coupling.

During the past week, the real EXDEV installation either passed or was not reached. The target instead failed in dashboard forwarding, listener cleanup, pairing, workspace restoration, and recreation.

The current failure reproduced six times after #11427. The test configures a generated wrapper as `NEMOCLAW_OPENSHELL_BIN`. That wrapper delegates to canonical OpenShell. The fail-closed forward ownership check correctly rejects the canonical listener because the configured executable is the wrapper.

The target now acts as a canary for several deterministic subsystems. A passing run spends about seven seconds on the core EXDEV operation inside a lifecycle that takes about twenty minutes.

## Goal

Keep this live E2E focused on behavior that requires real Docker, OpenShell, filesystem, process, and sandbox boundaries.

For each repair under this issue, move deterministic behavior to the smallest stable test lane before removing it from live E2E. Complete this issue when the live target owns only the accepted lifecycle outcomes and every removed condition has a deterministic owner or a documented no-value disposition.

## Retained live outcomes

The live target must continue to prove:

- The current custom image onboards and exposes plugin v1.
- The source and plugin destination have different device IDs.
- Real `openclaw plugins install --force` succeeds across that boundary.
- The installed payload works after a real gateway restart.
- Plugin v2 works after sandbox recreation.
- Cleanup removes the resources owned by the test.

These outcomes preserve the accepted scope in #10517 and Discussion #6108.

## Work

- [ ] Record the current direct and transitive assertion count, phases, and runtime baseline.
- [ ] Add a deterministic regression for the wrapper and canonical-listener ownership mismatch.
- [ ] Remove the generated wrapper from the forward lifecycle without weakening ownership verification.
- [ ] Prefer canonical OpenShell with a stable read-only host mount for the EXDEV source if a focused probe proves that it preserves the custom-image and recreation contract.
- [ ] If the host mount cannot preserve that contract, separate sandbox-create command authority from forward ownership authority through the narrowest existing dependency seam.
- [ ] Move wrapper behavior, image handoff, command construction, retry classification, diagnostics, cleanup ordering, and output normalization into `e2e-support`.
- [ ] Keep forward-owner matching and listener cleanup in source unit tests.
- [ ] Keep onboarding forward start, reuse, rejection, and recreation state restoration in integration tests.
- [ ] Remove manual listener termination and listener-identity assertions from this target after lower-level coverage owns them.
- [ ] Map changes to forward ownership, dashboard onboarding, and the EXDEV harness to the shortest relevant deterministic tests.
- [ ] Make those paths select this live target only when a real external boundary changed.

## Constraints

- Do not weaken fail-closed forward ownership.
- Do not add retries, random ports, or broad failed-job reruns for deterministic failures.
- Do not add general production support for wrapper chains without a separate accepted product decision.
- Do not remove custom-image, restart, or recreation coverage without a new scope decision.
- Do not move assertions into helpers, aggregate checks, snapshots, or generated probes only to reduce the count.
- Preserve redacted diagnostics, failure classification, and cleanup evidence.

## Acceptance criteria

- [ ] A deterministic test fails for the current wrapper and listener composition before the repair and passes after it.
- [ ] Every removed live condition has one disposition from #10920: already covered, moved earlier, covered by retained behavior, or no quality value.
- [ ] The pull request reports direct and transitive before-and-after assertion counts.
- [ ] The live target contains only the retained outcomes listed above.
- [ ] No E2E test case, target, job, negative behavior, recovery behavior, cleanup behavior, or security outcome is removed.
- [ ] Focused unit, integration, and `e2e-support` tests pass.
- [ ] The focused live target passes on its first attempt against the latest PR commit.
- [ ] A subsequent automatic main run executes and passes the target. A skipped target is not passing evidence.

## Related work

- Parent: #10920
- Prior pruning: #10517 and #10697
- Fixture repair: #10808 and #10972
- Forward and recreation repair: #11325
- Change that exposed the current mismatch: #11427
- Current failure: https://github.com/NVIDIA/NemoClaw/actions/runs/34596765622/job/103254852127
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3d7bcbf77efb9350c2a77e0d3c5dc8667063a867`.  There
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
{"case_id": "NVIDIA_NemoClaw__11547__3d7bcbf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
