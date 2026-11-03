# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Bound Portable startup waits with a shared monotonic deadline

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

Individually valid startup waits can exceed the caller's total allowance. Forward polling also uses wall-clock time, so a backward clock change extends its deadline.

At `e9cf24220532e33e704298632d9006b30254efdd`, a 55-second start followed by permitted exec-ready attempts exceeded 120 seconds. An injected 1,000 ms backward clock change extended a nominal 100 ms forward wait to approximately 1,100 ms.

## Reproduction

Exercise lifecycle recovery with controlled phase durations. Exercise forward polling with a backward wall-clock change and separately advancing monotonic time.

## Acceptance

- Establish an explicit end-to-end startup allowance at the owning operation boundary.
- Pass the remaining allowance into start, exec readiness, health, and relevant forward waits.
- Use monotonic elapsed time for deadlines.
- Preserve necessary cleanup on timeout and report the exhausted phase.
- Test total-budget exhaustion, clock rollback, prompt success, and timeout rollback.

Confirm the caller's actual contract before choosing a default. The 120-second reproduction is not a universal startup specification. This issue does not establish a 20-second or 27-second GFN performance promise.


## Recorded evidence

A 55-second start and individually valid exec-ready attempts exceeded 120 seconds together. A 1,000 ms backward wall-clock change extended a nominal 100 ms forward deadline to approximately 1,100 ms.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/onboard/experimental/hermes-portable-lifecycle.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/onboard/experimental/hermes-portable-lifecycle.ts)
- [Behavior owner: `src/lib/adapters/openshell/forward-service.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/adapters/openshell/forward-service.ts)

## Related work

Coordinate with the forward-process fix for the shared service. Preserve existing monotonic lease expiration checks.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `02d9198fde7e012257c65b6529a9e05f02a2fb1a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11652__02d9198",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
