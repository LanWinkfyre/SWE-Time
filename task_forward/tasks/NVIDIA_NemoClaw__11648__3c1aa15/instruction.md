# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Handle forward spawn errors and report early child exit

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

A failed forward spawn can terminate Node after the caller catches the startup failure. An early child exit is instead reported as a bind timeout.

Real child-process tests at `e9cf24220532e33e704298632d9006b30254efdd` reproduced ENOENT and EACCES. Both emitted an unhandled child error after the synchronous catch. A child that exited immediately with a nonzero status survived the caller path but lost its direct exit cause.

## Reproduction

Run a child-process harness around the current forward-service implementation with a missing executable, a non-executable file, and `/usr/bin/false`. Capture caller output, process exit status, and elapsed time.

## Acceptance

- Handle child errors from spawn through cleanup without an unhandled event.
- Detect early exit and report its cause before the bind deadline expires.
- Preserve successful bind qualification and process ownership checks.
- Clean up only children owned by the operation.
- Verify all three failures in real subprocesses, plus successful startup and foreign-listener refusal.

Affected code: `src/lib/adapters/openshell/forward-service.ts`. Evaluate event-loop blocking and caller contracts when choosing the fix.


## Recorded evidence

Both ENOENT and EACCES produced an unhandled child error after the caller caught the startup failure; the enclosing Node process exited 1. An immediate nonzero child exit was instead reported as a bind timeout.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/adapters/openshell/forward-service.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/adapters/openshell/forward-service.ts)

## Related work

Coordinate with open PR #11594 / issue #9808, which centralizes forward lifecycle ownership. Its current diff adds a new adapter and has not migrated all production consumers. This issue tracks the reproduced child-process failures in the current service.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3c1aa158fd38a9548f711ac345746c57aa73d5ee`.  There
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
{"case_id": "NVIDIA_NemoClaw__11648__3c1aa15",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
