# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
jest/vitest parity: literal X/__mocks__ imports diverge on the /__mocks__ virtual package suffix suppression

### Problem

The Vitest plugin suppresses unlisted-dependency findings for package names ending in `/__mocks__` via `virtual_package_suffixes` (`crates/core/src/plugins/vitest.rs`). The Jest plugin has no such suppression, so the same user-written literal import of a `__mocks__` path is reported as an unlisted dependency under Jest and stays clean under Vitest.

Measured: a test importing `@acme/__mocks__/server` literally is flagged `unlisted-dependency` (`@acme/__mocks__`) in a Jest project and suppressed in a Vitest project, identically before and after #2213 (which only removed the synthesized speculative candidates, not user-written imports).

### Decision needed

Either generalize the suffix suppression so Jest and Vitest treat literal `X/__mocks__` imports the same, or narrow the Vitest suppression now that #2213 removed the synthesized-candidate source of these names (the existing `vitest-mocks-virtual` fixture pins the current Vitest behavior, so narrowing is a deliberate behavior change).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95728543e804a0e4a4a0ca9dd239f328c6adde4d`.  There
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
{"case_id": "fallow_rs_fallow__2226__9572854",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
