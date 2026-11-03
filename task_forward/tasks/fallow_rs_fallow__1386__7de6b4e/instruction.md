# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Duplication flags test + generated files by default, creating false positives on hand-coded projects

## Summary

Running `fallow dupes` on a hand-coded project surfaces duplication that is almost always noise: test files (legitimately repetitive), auto-generated files, and structurally-similar data definitions. Users have to discover and hand-add ignores before the dupe report is trustworthy.

Real-world signal: in the Web Dev Simplified walkthrough ("This Tool Forces AI To Write Good Code", ~127k views), the reviewer ran dupes on a handwritten project and immediately hit false positives from (1) test files ("most of your tests are going to be duplicated code"), (2) generated TypeScript, and (3) card-definition data files (each unique, lots of shared boilerplate). A meaningful chunk of the video was spent configuring ignores to get a usable report.

## Current behavior

The dupe scan has built-in ignores only for generated framework output dirs, not for tests or generated source files:

`crates/core/src/duplicates/mod.rs:49`
```rust
pub const DUPES_DEFAULT_IGNORES: &[&str] = &[
    "**/.next/**", "**/.nuxt/**", "**/.svelte-kit/**", "**/.turbo/**",
    "**/.parcel-cache/**", "**/.vite/**", "**/.cache/**", "**/out/**",
    "**/storybook-static/**",
];
```

Test files are excluded only via `--production` mode (global, opt-in, broader than just dupes), not from the default dupe scan. The docs acknowledge the friction but punt to manual `dupes.ignore` config.

## Options (pick a direction)

1. **Extend `DUPES_DEFAULT_IGNORES` with test patterns (S):** add `**/*.test.*`, `**/*.spec.*`, `**/__tests__/**`, `**/__mocks__/**`, mirroring the proven `--production` exclude set. Opt-out already exists via `duplicates.ignoreDefaults: false`.
   - Tradeoff: hides intra-test duplication (which some users want to refactor into helpers). Defensible as a default since the dupe report's value is mostly in non-test code and it is one flag to re-enable.
2. **Auto-detect generated files (M):** skip files with a generated marker (`@generated` header, common `*.gen.ts` / `*.generated.*` names). Heuristic, needs care to avoid false skips.
3. **Ship a documented "recommended dupes ignore" preset (S)** instead of changing defaults, so behavior stays explicit.

Recommendation: do (1) now (biggest noise reduction, lowest risk, has an opt-out), consider (2) as a follow-up, keep (3) as the conservative fallback if changing defaults is undesirable.

## Acceptance (for option 1)

- `fallow dupes` on a project with `*.test.ts` files reports no test-vs-test duplication by default.
- `duplicates.ignoreDefaults: false` restores scanning of test files.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7de6b4ee07eb2635621af39a10e120bd8b75db8b`.  There
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
{"case_id": "fallow_rs_fallow__1386__7de6b4e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
