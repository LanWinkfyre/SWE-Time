# Recover the symbolic verification state this change produces

A regression report was filed against `ZSWatch/ZSWatch`.  The report is quoted verbatim below.

## Report

```
Dead link in readme

Under demos: [HTTP requests over BLE through Gadgetbridge](https://github.com/jakkra/ZSWatch/assets/4318648/12d6e754-ceb3-4efd-9a75-d207aaeb0e82)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ea6dd0ad787ef509bae0f001334d7b69bdd6b5ef`.  There
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
{"case_id": "ZSWatch_ZSWatch__472__ea6dd0a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
