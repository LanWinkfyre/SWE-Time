# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Android is not supported

## Summary

- OS: Android 10
- Architecture: aarch64
- Psutil version: 7.0.0
- Python version: 3.12.10
- Type: installation

<img width="1105" height="965" alt="Image" src="https://github.com/user-attachments/assets/1db26251-779f-46ed-a36d-23aa7f5f70b9" />
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5fcc850ec27c34162a2b6746157e0fed189bf199`.  There
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
{"case_id": "giampaolo_psutil__2611__5fcc850",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
