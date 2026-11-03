# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Surface a workspace diagnostic when override resolution is skipped for bun.lockb-only repos

Since #2341 (PR #2350), when the only lockfile next to `package.json` is bun's legacy binary `bun.lockb`, `unused_dependency_overrides` emits nothing: resolution ground truth is unreadable and declaration-only analysis would produce the exact false positives the issue was about. That suppression is currently silent.

A user with only `bun.lockb` gets no findings and no explanation. Proposal from the PR #2350 review: a workspace diagnostics entry (new `WorkspaceDiagnosticKind` variant) stating that override resolution was skipped because only `bun.lockb` was found, with the hint to run `bun install --save-text-lockfile` (bun 1.2+) to produce a text `bun.lock`. Needs output-schema and contract surface regeneration (MCP and agent docs) along with the docs-site note in the companion documentation repository.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4a025be9b173bc8c29c2b2c121432ab97bc7dacd`.  There
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
{"case_id": "fallow_rs_fallow__2358__4a025be",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
