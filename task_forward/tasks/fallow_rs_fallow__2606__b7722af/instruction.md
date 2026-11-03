# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
coverage analyze --cloud: the static index skips callee-named callbacks, getters and object members, so they never match

Follow-up to #2593. With the cloud now hashing function identities over repo-relative paths, `fallow coverage analyze --cloud` matches directly on `stable_id` for every function the local static index knows. On a 1,780-function Bun/Elysia service that still leaves `cloud_functions_unmatched: 606`, and the unmatched set is a consistent class rather than a residue:

- callbacks the instrumenter names after their callee: `find` (36.8M invocations), `filter` (21.2M), `map`, `references` (Drizzle column callbacks, 27 of them), `sqliteTable` (25 table callbacks), `transaction` (33), `scheduleEmailTask`, `mapWithConcurrency`, `setInterval`, `onBeforeHandle`;
- getters and object-literal members (`get closed`, `execute`, `rollback` on a returned client object);
- `(anonymous_N)` callbacks the instrumenter could not name (95).

These are real functions with real production traffic; the health/complexity pass that feeds the static index (`crates/cli/src/coverage/analyze.rs`, the `StaticFunctionInfo` construction from `FunctionComplexity`) does not enumerate them, so nothing on the local side can match them and the CLI silently drops the hottest callbacks in the service.

### What to do

1. Enumerate every function-like node the instrumenter would emit: arrow and function expressions passed as call arguments (named after the callee, matching the `nameCallbackArguments` convention of `oxc-coverage-instrument`), object-literal methods and getters (named after the key), class members, and unnamed callbacks with the same `(anonymous_N)` numbering per file the instrumenter uses. The identity recipe (path, name, line) must produce the same `stable_id` the cloud stores for those rows.
2. Keep the complexity pass untouched; add the extra entries to the static index only, flagged as `callback` so verdict copy can say "callback passed to X" instead of treating it like a declaration.
3. Add a fixture with a Drizzle-style schema (`sqliteTable("t", { ... }, (table) => [...])`, `.references(() => ...)`), an object returned from a factory with methods and a getter, and a `.map(...)` chain, plus a cloud payload naming them the instrumenter's way; assert all of them match.

### Acceptance

- On the service above, `cloud_functions_unmatched` drops to the `(anonymous_N)` rows only, and `hot_paths` includes the `find` and `filter` callbacks with their invocation counts.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b7722aff930fdad053d4d811b8e5fb055ff1ef44`.  There
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
{"case_id": "fallow_rs_fallow__2606__b7722af",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
