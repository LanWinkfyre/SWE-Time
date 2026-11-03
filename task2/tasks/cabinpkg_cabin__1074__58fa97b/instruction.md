# Recover the symbolic verification state this change produces

A regression report was filed against `cabinpkg/cabin`.  The report is quoted verbatim below.

## Report

```
[Feature Request] `cabin remove`

For some reason this feature went unnoticed, I realized this now after having to remove the dependency from both .toml and the cache folder where the lib's git repository is cloned.

off-topic: you need to add a template for feature request
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `58fa97b4e3dbf568426646840ed056ff34bdad4a`.  There
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
{"case_id": "cabinpkg_cabin__1074__58fa97b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
