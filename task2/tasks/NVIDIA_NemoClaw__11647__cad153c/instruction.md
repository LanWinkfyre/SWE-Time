# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Release lifecycle mutation locks before waiting for an interactive launch session

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

Launch retains lifecycle mutation locks until the interactive session ends. Concurrent lifecycle commands can block or time out while the user is at the prompt.

Three regression cases fail at `e9cf24220532e33e704298632d9006b30254efdd`: accepted Hermes launch, prepared Hermes launch, and ordinary prepared launch. A separate real-process host-fence contender timed out after approximately 12 seconds.

## Reproduction

Start an interactive launch with a controlled session-completion promise. Keep the session open. Start a mutation-lock contender and assert that it can enter after launch setup completes. Test the action and public CLI wrapper separately.

## Acceptance

- Retain locks during qualification and mutable launch setup.
- Release both the action lock and outer CLI fence before waiting for interactive completion.
- Preserve exit status, session cleanup, and startup failure handling.
- Pass all three regressions and a real-process contention check.

Affected code: `src/lib/actions/sandbox/launch.ts` and `src/lib/cli/nemoclaw-oclif-command.ts`. The connect flow provides an existing separation between setup and session waiting.


## Recorded evidence

Three controlled interactive-session tests failed: accepted Hermes launch, prepared Hermes launch, and ordinary prepared launch. A separate process waiting for the host fence timed out after approximately 12.05 seconds.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/actions/sandbox/launch.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/actions/sandbox/launch.ts)
- [Behavior owner: `src/lib/cli/nemoclaw-oclif-command.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/cli/nemoclaw-oclif-command.ts)

## Related work

Related lock-domain epic: #9955. This issue is limited to lock lifetime across an interactive session.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cad153cc1b761353e4a9590da7fa2f5121913056`.  There
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
{"case_id": "NVIDIA_NemoClaw__11647__cad153c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
