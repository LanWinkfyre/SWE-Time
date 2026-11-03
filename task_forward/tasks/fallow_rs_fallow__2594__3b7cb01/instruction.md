# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
coverage analyze --production: test-only exports get safe_to_delete

With `--production`, `fallow coverage analyze --cloud` labels exports that are only referenced by test files as `safe_to_delete`. On a real service the top of the list is `__resetMemoryPacingForTests`, `__resetMemoryProbeForTests`, `resetResendCacheForTests`, `resetRateLimitStateForTests`, `__resetAdoptionStatsCache` and similar helpers: 36 findings, all high confidence, evidence `static_status: unused`, `test_coverage: not_covered`. A user who follows the verdict deletes them and breaks the test suite.

### Why it happens

`--production` removes test files from the graph before `unused.function_is_used(path, name, line)` runs (see the `static_used` field on `StaticFunctionInfo` in `crates/cli/src/coverage/analyze.rs`), so a test-only export reads as statically unused. Combined with zero production invocations that satisfies the `safe_to_delete` rule.

### What to do

1. Keep a second, non-production reachability answer per function (or a cheap "referenced from a test file" bit) and expose it in the finding evidence, for example `evidence.test_only_reference: true`.
2. When a function is statically unused in production but referenced from tests, downgrade the verdict to `review_required` and add an action text along the lines of "only tests reference this export; delete the test usage together with the function or keep it".
3. Cover it with a unit test: a project with `export const resetForTests = ...` used only from `*.test.ts`, analysed with `--production`, must not produce `safe_to_delete`.

### Acceptance

- No `safe_to_delete` verdict for an export that a test file references.
- The human, JSON and review outputs all carry the new evidence bit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3b7cb01a1e4cdff6f3a9d700c7cddce7178bebad`.  There
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
{"case_id": "fallow_rs_fallow__2594__3b7cb01",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
