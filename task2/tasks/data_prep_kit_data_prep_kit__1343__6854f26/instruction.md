# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Feature] Enforce Folder boundaries when resizing files

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

transforms/resize

### Feature

Goal: When running the resize transform, do not allow files from different subfolder to be merged and do not split files across multiple subfolders.


### Are you willing to submit a PR?

- [x] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6854f26d56875cc0f003b2251cfa58a7e4d360be`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `dev`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "data_prep_kit_data_prep_kit__1343__6854f26",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
