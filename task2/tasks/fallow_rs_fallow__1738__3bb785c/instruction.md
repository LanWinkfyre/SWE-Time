# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Detect dev dependencies used in production (promote-side mirror of test-only/type-only-dependency)

### Problem

Fallow detects dependency *demotion* drift but not *promotion* drift.

Two sibling rules already flag a production dependency that belongs in `devDependencies`:

- `test-only-dependency` — "Production dependencies only imported from test files … can move to devDependencies."
- `type-only-dependency` — "Production dependencies only imported via `import type` … can move to devDependencies."

The mirror is missing: a package in **devDependencies** that is imported by **production** (non-test, non-config) source code with a **runtime/value** import should be **promoted to `dependencies`**. A production-only install (`pnpm install --prod`) omits devDependencies, so the import breaks at runtime — and nothing currently catches it.

**Reproduce:**

```jsonc
// package.json
{ "devDependencies": { "yaml": "^2.0.0" } }
```

```ts
// src/lib/config.ts (reachable production code)
import { parse } from "yaml";
export const load = (s: string): unknown => parse(s);
```

```
$ fallow dead-code --fail-on-issues
✓ No issues found            # exit 0
```

`unlisted-dependency` does **not** fire, because the package *is* listed — just under the wrong section. Contrast: a `dependency` imported only from a test correctly reports `test-only-dependency` and exits 1. The promote path is the absent mirror.

### Proposed solution

A new rule (suggested `dev-dependency-in-production`) that reuses the existing prod-vs-test file partition and per-import value/type accounting from the sibling detectors:

- Flag a `devDependencies` entry when ≥1 **production** source file imports it via a **runtime/value** import.
- Do **not** flag when the only production imports are type-only (`import type`) — types are erased at build time (mirrors `type-only-dependency`).
- Do **not** flag imports coming only from test/config files (that's `test-only-dependency`'s job).
- Skip workspace packages, known tooling (`@types/*`, `typescript`, …), `ignoreDependencies` entries, and packages also declared in `dependencies` / `peerDependencies` / `optionalDependencies` (provided at runtime by another manifest section).
- Default severity `warn`, matching the sibling dependency-family rules.

This is the inverse of `test-only-dependency` and hooks into the same production-mode file classification (issues #182 / #111 / #1055, PR #1059).

### Alternatives considered

- **`unlisted-dependency`** already covers *unlisted* packages, but not *mis-sectioned* ones, so it cannot detect this case.
- Leaving it to `pnpm install --prod` + a runtime crash in CI — that's exactly the late, expensive failure a static check should pre-empt.

I have an implementation ready that follows the analyzer-authoring guide (detection + issue-type enum + config rule + all output formats + `fallow explain` + LSP + CI jq summaries + generated contracts + fixtures/tests). PR to follow.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3bb785ce9a64066a096f33379e34b2b7a3e0c31c`.  There
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
{"case_id": "fallow_rs_fallow__1738__3bb785c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
