# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dead-code --trace reports a value export as unused when its only credit is a bound import type of a const-only export

`fallow dead-code` credits a value-only export referenced through `import type { helper }` (the type lane falls back to the value declaration when no type declaration exists), so the export is not reported. `fallow dead-code --trace <file>:<export>` prefers the value namespace for a value export (`trace_prefers_the_value_namespace_independent_of_usage` in `crates/engine/src/trace_impl.rs`), finds no value-lane reference, and prints `is_used: false`, `direct_references: []`. An agent following the "run `dead-code --trace` before deleting" guidance gets two contradictory answers for the same export.

## Reproduction

`package.json`: `{"name":"probe","type":"module","main":"src/index.ts"}`

```ts
// src/index.ts
import type { helper } from './impl';
export type T = typeof helper;

// src/impl.ts
export const helper = (): number => 1;
```

- `fallow dead-code --format json --quiet --no-cache`: no unused exports.
- `fallow dead-code --trace src/impl.ts:helper --format json --quiet --no-cache`: `namespace: value`, `is_used: false`, `direct_references: []`.

The ambient star shapes from #2357 do not trigger this (trace on the #2357 fixture exports reports the crediting reference). The trigger is any bound type-only import whose credit lands on a value declaration through the type-lane fallback.

## Possible direction

When the value lane carries no references, fall back to the type lane and report `namespace: "type"` with those references, or report both lanes. Trace JSON is a public contract, so the change needs snapshot updates and a backwards-compatibility note.

Surfaced while reviewing #2363 (the fix for #2357).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0a95caca69955029a0c41c397f01f2b6b87b1b2f`.  There
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
{"case_id": "fallow_rs_fallow__2371__0a95cac",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
