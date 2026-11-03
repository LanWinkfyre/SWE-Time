# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Feature] Add support for Python 13, 14

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

Other

### Feature

pip install does not work for python > 12

### Are you willing to submit a PR?

- [ ] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f5a181432820243dc515289dfa14ec46fa439e00`.  There
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
{"case_id": "data_prep_kit_data_prep_kit__1524__f5a1814",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
