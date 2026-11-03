# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
export { default } from and import { default as X } never credit the target's default export

`handle_import_specifier` and the ambient named re-export branch in `crates/extract/src/visitor/visit_impl.rs` record `ImportedName::Named("default")` for a `default` specifier, and `ExportNameIndex::matches` (`crates/graph/src/graph/build.rs`) looks it up in the named map, where `ExportName::Default` is never indexed, so the default export keeps reporting as unused.

## Reproduction

`package.json` main `src/index.ts`:

```ts
// src/index.ts
import { default as X } from './impl';
export const app = X;

// src/impl.ts
export default function dflt(): number { return 1; }
export const untouched = 2;
```

`fallow dead-code --format json --quiet --no-cache` reports `impl.ts:default`.

The same happens for `declare module 'pkg' { export { default } from './impl' }` and for `export { default as Impl, Y as Z } from './impl'` inside an ambient body (`Y` is credited, the default is not). Reproduces identically on the pre-#2357 binary, so this is pre-existing.

## Direction

Normalise a `default` specifier to `ImportedName::Default` in both producers, or make `ExportNameIndex::matches` map `Named("default")` onto the default slot, with a fixture covering `import { default as X }`, `export { default } from`, and `export { default as X } from` inside an ambient body. The `export * as ns` ambient path from #2363 already uses `ImportedName::Default` and is unaffected.

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
{"case_id": "fallow_rs_fallow__2374__0a95cac",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
