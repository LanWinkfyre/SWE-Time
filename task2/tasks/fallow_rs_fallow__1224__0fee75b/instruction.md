# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dupes: make ignoreImports the default — import blocks should never be reported as duplication

### Problem

`fallow dupes` reports import blocks as duplicated code unless `ignoreImports` is explicitly enabled. In any TypeScript codebase, similar files necessarily need similar imports, and formatters (Prettier, oxfmt, organize-imports) sort them into identical order. Token-identical import blocks are therefore a structural property of a well-formatted codebase, not copy-pasted logic — they should never surface as clone groups.

#113 added `ignoreImports: true` (v2.33.0), which works well — but as an opt-in. That means every new user's first run reports import blocks among the top clone groups, inflating the duplication percentage and creating noise until they discover the flag. A default that produces known false positives undermines trust in the rest of the report.

### Proposed solution

Flip the default to `ignoreImports: true`. Keep an opt-out (`"ignoreImports": false` / `--no-ignore-imports`) for anyone who wants the old behavior. Consider also filtering re-exports and CommonJS `require()` calls, which have the same property.

### VS Code extension

Relatedly, please expose this as an extension setting (e.g. `fallow.duplicates.ignoreImports`) so it can be configured from VS Code settings without requiring a `.fallowrc.json` in the repo. Extension settings could act as fallback defaults when no project config is present.

### Alternatives considered

Keeping it opt-in and documenting it more prominently — but defaults matter: the false-positive case (sorted imports) is near-universal in TypeScript projects, while the case where import duplication is a useful signal is rare.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0fee75b53ea35f1aef1cdd9dfc18e255392115cc`.  There
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
{"case_id": "fallow_rs_fallow__1224__0fee75b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
