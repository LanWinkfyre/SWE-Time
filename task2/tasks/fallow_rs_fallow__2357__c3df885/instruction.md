# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Ambient-module star re-exports and bare-specifier re-exports need a post-#2349 semantics decision

#2349 (PR #2351) made named re-exports inside `declare module '...'` bodies credit their target symbols without creating a file-level export surface. Two adjacent behaviors were deliberately left out and should get a decision:

1. **Star re-exports are now asymmetric.** `declare module 'pkg' { export * from './impl' }` still pushes a `ReExportInfo` onto the declaring file (`visit_export_all_declaration` is unchanged). Verified pre-#2351: when the ambient file is an entry point, a genuinely unused `export const helperA` in `./impl` is laundered into the entry's public surface and reported as used. Making `export *` symmetric is not a cheap fix: a side-effect edge carries no symbol, so a naive change drops credit for all target exports and flips false positives the other direction.

2. **Bare-specifier re-exports flip dependency classification.** `declare module 'x' { export { A } from 'some-dep' }` now emits a type-only import for `some-dep`. A package referenced solely through such an ambient re-export can newly emit a type-only-dependency finding advising a move to devDependencies. The type-space classification is defensible for an ambient body, but it is undecided and untested; a fixture should pin whichever classification is intended.

Both surfaced in the panel review of PR #2351.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c3df8857ec0fca10f1b359946ec89a0208a50715`.  There
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
{"case_id": "fallow_rs_fallow__2357__c3df885",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
