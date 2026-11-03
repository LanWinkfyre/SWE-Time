# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
improve unit tests for ogx library client

### 🤔 What is the technical debt you think should be addressed?

These are minor, but should be improved:
* `test_sync_client_shutdown_idempotent` calls `shutdown()` once (and the point is to check that the shutdown is idempotent.
* Several tests just check `hasattr()` + `callable()`. Do we even need them? 

### 💡 What is the benefit of addressing this technical debt?

Have unit tests actually test things for us 😉 

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `87ce1b416899fab862b714120d01007889d121b0`.  There
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
{"case_id": "ogx_ai_ogx__5772__87ce1b4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
