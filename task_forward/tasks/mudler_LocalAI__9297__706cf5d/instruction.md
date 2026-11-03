# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Add prompt to qwen-asr backend

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
When using qwen3-asr with qwen-asr backend through the API, only the filename and language are forwarded to the model. Given Prompts or Context is not forwarded to the model.

**Describe the solution you'd like**
Forward context to the qwen3-asr model.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `706cf5d43c324184b8e1df6e8141ce335c591b31`.  There
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
{"case_id": "mudler_LocalAI__9297__706cf5d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
