# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Whole-module consumers of a star barrel do not credit exports the barrel only exposes through export *

Two consumer shapes observe every name on a module object but only credit the module's direct exports: names that arrive through the module's own `export * from './deep'` are reported as unused.

## 1. Whole-object use of a namespace import

`package.json`: `{"name":"probe","type":"module","main":"src/index.ts"}`

```ts
// src/index.ts
import * as ns from './barrel';
export const all = Object.values(ns);

// src/barrel.ts
export * from './deep';
export const direct = (): number => 1;

// src/deep.ts
export const deepHelper = (): number => 2;
```

`fallow dead-code --format json --quiet --no-cache` reports `src/deep.ts:deepHelper`. The whole-object use routes to `mark_all_exports_referenced_at_site`, which covers the barrel's direct exports only.

## 2. Dynamic-import pattern targets

```ts
// src/index.ts
const mods = import.meta.glob('./mods/*.ts');
export const app = Object.keys(mods).length;

// src/mods/a.ts
export * from '../deep/a-deep';
export { namedOnly } from '../deep/a-named';
export const aOwn = 1;

// src/deep/a-deep.ts
export const deepStarOne = 1;
export const deepStarTwo = 2;

// src/deep/a-named.ts
export const namedOnly = 1;
export const namedSibling = 2;
```

(`package.json` main `src/index.ts`, devDependency `vite`.) Reported: `deepStarOne`, `deepStarTwo`, `namedSibling`. `namedSibling` is correct (not forwarded); the two star-forwarded names are false positives.

## Direction

#2363 fixed the same gap for ambient-module star re-exports with `ModuleGraph::collect_ambient_star_targets` in `crates/graph/src/graph/re_exports/mod.rs` (seeded from the ambient star symbols, following `export *` and `export * as` sources, consumed by `propagate_star_re_export` and `propagate_namespace_re_exports`). The runtime shapes need the same closure seeded from whole-object namespace uses and from dynamic-import pattern targets. Both shapes reproduce identically on the pre-#2357 binary, so this is pre-existing.

Surfaced while reviewing #2363 (the fix for #2357).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `dc03fd1484261a623e044e1dbe97378095bae4ac`.  There
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
{"case_id": "fallow_rs_fallow__2372__dc03fd1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
