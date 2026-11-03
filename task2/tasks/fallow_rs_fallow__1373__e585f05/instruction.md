# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dead-code false positive: named import through `export *` not credited for merged `const` + `declare namespace` export

## Summary

When a symbol is declared as a merged value + namespace (`export const X = Object.assign(...)` together with `export declare namespace X`) and re-exported through a star barrel (`export * from './x'`), `dead-code` reports `X` as an **unused export** even though a reachable module imports it by name through the barrel.

A plain `export const` re-exported the same way is resolved correctly, so the trigger is specific to the **merged value + namespace** declaration combined with `export *`.

**Version:** fallow 2.100.0

## Minimal reproduction

`merged.ts`
```ts
export declare namespace Merged {
  type Foo = string
}
export const Merged = Object.assign(function Merged() {}, {bar: 1})
```

`index.ts` (barrel)
```ts
export * from './merged'
```

`consumer.ts` (reachable from an entry point)
```ts
import {Merged} from './index'
void Merged
```

Run:
```
fallow dead-code
```

## Expected

`Merged` is reported as used (it has a named importer through the barrel).

## Actual

`Merged` is reported under **Unused exports**:

```
● Unused exports (1)
  merged.ts
    :4 Merged
  Exported symbols with no known consumers
```

## Conflicting signal from `--trace`

`fallow dead-code --trace "merged.ts:Merged"` reports the **opposite** — the importer edge *is* resolved here, but it is not credited by the unused-export pass:

```
USED Merged in merged.ts
  File: reachable
  Reason: Used by 1 file(s), re-exported through 1 barrel(s)
  1 direct reference(s):
    -> consumer.ts (named import)
  Re-exported through:
    -> index.ts as '*' (0 ref(s))
```

Note the barrel line: `as '*' (0 ref(s))`.

## Not reproduced by

A plain `export const plainThing = 42` re-exported via `export *` and imported the same way is correctly reported as **used**. Only the merged value + namespace export triggers the false positive.

## Workaround

Replacing the star re-export with a named one fixes it:

```ts
export {Merged} from './merged'
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e585f058e59b78b2d64339c7d16e380fbbcfc484`.  There
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
{"case_id": "fallow_rs_fallow__1373__e585f05",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
