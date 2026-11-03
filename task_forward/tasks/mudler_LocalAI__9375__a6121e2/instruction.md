# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Add option for LRU eviction on memory pressure / load


**Is your feature request related to a problem? Please describe.**
Usecase is that i have limited memory but want to test multiple models while still need to maintain certain smaller models always in memory.

**Describe the solution you'd like**
New Setting: LRU eviction on model load:

LRU eviction that fires whenever a new model /backend is about to be loaded, Triggers if the to be loaded model would not fit in memory (same calculation as on the model gallery). eviction target(s) are biggest models first, keep smaller ones in memory.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a6121e240e37d44b0cdde4dc6778dcf5df3e15b5`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__9375__a6121e2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
