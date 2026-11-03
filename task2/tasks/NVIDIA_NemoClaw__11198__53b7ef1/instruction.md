# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Flaky test] sandbox readiness first-observation timeout asserts an exact 6000 ms against the real clock

## Description

`src/lib/onboard/sandbox-readiness-tracing.test.ts` asserts an exact millisecond value for the first adaptive observation timeout, but reads the real clock to compute it. On a loaded CI runner the value comes back one millisecond low and the shard fails.

The test is otherwise fully deterministic — the observer is replayed and `sleep` is mocked — so this is the only real-time dependency in it.

## Evidence

Observed on `cli-test-shards (6)` (PR #10261, run `34180924830`):

```
AssertionError: expected 5999 to be 6000 // Object.is equality
```

The same test file passed 5/5 consecutive local runs on the same commit, and the PR's diff at the time touched a single unrelated import in `src/lib/actions/inference-get.ts`. A rerun of the shard passed with no code change.

The assertion is `src/lib/onboard/sandbox-readiness-tracing.test.ts:93`:

```ts
expect(observationTimeouts[0]).toBe(6_000);
```

## Root cause

`createSandboxReadyWaiter` is constructed in that test without a `now` dependency, so the readiness budget falls back to the real clock:

- `src/lib/onboard/readiness-wait.ts:46-47` — `const sourceNow = options.now ?? Date.now; const startedAt = sourceNow();`
- `src/lib/onboard/readiness-wait.ts:79` — `deadlineMs: startedAt + budgetMs`
- `src/lib/onboard/sandbox-readiness-tracing.ts:154-156` — each observation timeout is `Math.max(1, Math.floor(deadlineMs - now()))`

So the first observation only receives the full `6000` when strictly less than 1 ms of wall-clock time passes between the deadline being established and the first observation being issued. That covers `createReadinessWaitOptions` setup, entry into `waitUntilAsync`, and `settleSandboxObservation`. Sub-millisecond locally, occasionally over 1 ms on a busy shard runner, which yields `Math.floor(6000 - 1) = 5999`.

Nothing is wrong with the production behavior here — a slightly reduced first timeout is the intended effect of an absolute deadline. Only the exact-equality assertion is unsafe.

## Impact

An unrelated PR can go red on any shard that happens to contain this file, which costs a rerun cycle and makes real regressions easier to overlook. It also produces a confusing signal, since the failure text mentions no test name in the GitHub annotation.

## Suggested fix

`SandboxReadyWaitDeps` already accepts an injectable `now` (`src/lib/onboard/sandbox-readiness-tracing.ts:124`), and the whole point of that seam is deterministic tests. Passing a fixed clock into `createSandboxReadyWaiter` in this test keeps the exact-value assertion meaningful and removes the race:

```ts
const waitForSandboxReady = createSandboxReadyWaiter({
  observer,
  target: TARGET,
  isLinuxDockerDriverGatewayEnabled: () => true,
  sleep,
  now: () => 0,
});
```

A tolerance-based assertion would also stop the flake, but it would weaken the check; injecting the clock keeps the full-budget contract pinned exactly.

Worth checking whether sibling tests in the same file, and other users of `createReadinessWaitOptions`, share the same real-clock dependency.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `53b7ef1672f6f390b60fee9d04078a176422dfdf`.  There
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
{"case_id": "NVIDIA_NemoClaw__11198__53b7ef1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
