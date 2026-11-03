# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Roll back an owned forward when the second forward fails to start

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

When the first required forward starts and the second fails before spawn, the first remains active. The current rollback deliberately refuses name-based stopping because it cannot prove process continuity.

The two-forward regression fails at `e9cf24220532e33e704298632d9006b30254efdd`. This is an ownership limitation; removing the conservative check would make cleanup unsafe.

## Reproduction

Start the first forward in a controlled recovery transaction. Fail the second before spawn. Assert that recovery fails and removes only the first forward created by this transaction.

## Acceptance

- Retain sufficient ownership evidence to roll back a forward created by the current transaction.
- Preserve preexisting forwards and replacement processes.
- Reject cleanup after PID reuse, identity drift, or unverifiable ownership.
- Make retry safe after partial startup and partial cleanup.
- Pass the existing two-forward regression and ownership-race tests. Add a disposable real-process check where the API supports it.

Affected code: `src/lib/actions/sandbox/probe/hermes-portable-forward-recovery.ts` and its adapter boundary. Coordinate with the forward-process issue without combining their PRs.


## Recorded evidence

The first forward remained after the second forward failed before spawn. The assertion requiring removal of only the newly created first forward failed.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/actions/sandbox/probe/hermes-portable-forward-recovery.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/actions/sandbox/probe/hermes-portable-forward-recovery.ts)

## Related work

Coordinate with #11594 / #9808 for an ownership-safe cleanup capability. Related #11411 concerns onboarding failing to establish port 8642; this issue instead begins with one successfully created forward and tests partial transaction cleanup. PR #11549 concerns owned-forward reuse during recreation.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ebb5e7555550cd43ea8de3e2bf6730f1534a0bf2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11649__ebb5e75",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
