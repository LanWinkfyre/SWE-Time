# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dupes: extend ignoreImports to also exclude re-export barrels and require() blocks

### Background

[#1224](https://github.com/fallow-rs/fallow/issues/1224) made `ignoreImports` the default for `fallow dupes`: token-identical ES `import` declarations are excluded from clone detection because sorted import blocks are a formatting artifact, not copy-paste. That fix is intentionally scoped to ES `import` declarations only.

### Problem

Two related constructs have the same structural property but are still counted as clone candidates:

- **`export ... from` re-export barrels.** `index.ts` files that are pure `export { x } from './x'` / `export * from './y'` blocks are common in libraries, NestJS/Express, and component packages. Two token-identical re-export barrels can surface as a clone group.
- **CommonJS `require()` blocks.** A run of `const x = require('...')` lines has the same sorted-similarity property as an ES import block.

The result is a half-state: after #1224, identical ES import blocks go quiet but identical re-export barrels and `require()` blocks still report, which can read as inconsistent.

### Proposed direction

Extend what `ignoreImports` strips to also cover `export ... from` re-export declarations and top-level `require()` binding blocks, so the knob covers the full "module wiring is not duplication" intent.

### Notes / open questions

- This changes what the existing flag *filters*, so it affects projects that already set `ignoreImports: true`, not only the new default. Needs benchmark validation on the real-world fixtures and a false-positive pass (re-export edges are graph-relevant elsewhere; this only affects the duplication tokenizer).
- Worth deciding whether re-exports and `require()` should be one combined toggle (current `ignoreImports`) or separately controllable.

Tracked as the phase-2 follow-up to #1224.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8c26b85369db46e2d00234d19aa8825475b07618`.  There
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
{"case_id": "fallow_rs_fallow__1225__8c26b85",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
