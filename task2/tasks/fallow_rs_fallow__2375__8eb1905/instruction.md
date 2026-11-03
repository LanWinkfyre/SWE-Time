# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
export type * inside a declare module body still creates a file-level type-only star re-export

#2363 routes `export *` and `export * as ns` inside an ambient body through a whole-module import so the declaring file gains no export surface, but `export type * from './impl'` (and `export type * as ns`) keeps the pre-existing file-level type-only star re-export: the whole-module import shape carries no type modifier, and routing the type-only star through it would credit the value meaning of every target export.

## Observed (identical before and after #2363)

```ts
// src/pair.ts
export interface Foo { a: number }
export const Foo = 1;
export const plain = 3;
export default function d(): void {}

// src/shim.ts (non-entry, imported for side effects by the entry)
declare module 'pkg' { export type * from './pair' }
export {};
```

Reported: `pair.ts:Foo` (interface and const), `plain`, and `default`. The interface half is a false positive because the type star forwards it.

With the declaration in the entry-point `ambient.d.ts` instead, the file-level star launders the consts (`Foo` const, `plain`) into the entry surface and only `default` reports: a false negative.

## Direction

Give the extractor a way to record a type-only whole-module import (a flag on `ImportInfo`, which needs an extract cache bump and constructor updates) so the graph can mark the star surface in the type lane only, skipping defaults and crediting `interface Foo` without `const Foo`. Rare form; the extract test `ambient_module_type_only_star_re_export_keeps_file_level_shape` pins the current shape so the change is deliberate when it lands.

Surfaced while reviewing #2363 (the fix for #2357).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8eb190505e6a310544e897eb841dc398dac73e36`.  There
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
{"case_id": "fallow_rs_fallow__2375__8eb1905",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
