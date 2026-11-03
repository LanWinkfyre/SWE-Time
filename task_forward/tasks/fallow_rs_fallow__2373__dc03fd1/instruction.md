# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Entry-point export * as sub chains stop at the first namespace level

For a real entry point the namespace re-export phase credits every direct export of an `export * as sub` source, but neither `sub`'s own `export * from './deep'` sources nor its own `export * as sub2 from './sub2'` sources, because `collect_entry_star_targets` only walks plain `export *` edges from entry barrels and `propagate_namespace_re_exports` only treats entry points themselves as exposing a namespace.

## Reproduction

`package.json`: `{"name":"probe","type":"module","main":"src/index.ts"}`

```ts
// src/index.ts
export * from './barrel';

// src/barrel.ts
export * as sub from './sub';
export const direct = 1;
export default function barrelDefault(): void {}

// src/sub.ts
export * from './deep';
export * as sub2 from './sub2';
export const subOne = 1;
export default function subDefault(): void {}

// src/deep.ts
export const deepX = 1;
export default function deepDefault(): void {}

// src/sub2.ts
export const sub2X = 1;
export default function sub2Default(): void {}
```

`fallow dead-code --format json --quiet --no-cache` reports `deep.ts:deepX`, `deep.ts:default`, `sub2.ts:sub2X`, `sub2.ts:default` (plus the correct `barrel.ts:default`). Everything on `sub` is reachable through the entry's namespace object (`deepX` via `sub.deepX`, `sub2X` and `sub2`'s default via `sub.sub2`); `deep.ts:default` is correctly reported because `sub`'s plain `export *` never forwards it.

## Direction

#2363 implemented exactly this closure for ambient star targets (`ModuleGraph::collect_ambient_star_targets` follows `imported_name == "*"` edges recursively; members get entry-star treatment for `export *` sources and namespace exposure for `export * as` sources). Extending the entry-point seed to walk `export * as` edges the same way closes the gap. Reproduces identically on the pre-#2357 binary, so this is pre-existing.

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
{"case_id": "fallow_rs_fallow__2373__dc03fd1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
