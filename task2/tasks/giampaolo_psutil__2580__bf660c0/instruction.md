# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[CI] CI built wheels are not tested

## Summary

- OS: All
- Architecture: All
- Psutil version: master
- Python version: All
- Type: ci, tests, wheels

## Description

CI built wheels are not tested since d7b2f188618de95c4af30168437d5d2fd4e5fa83
The commit factorizes some test code which has for effect to test an in-place build of the extensions rather than test the wheel just built in CI. see the logs in https://github.com/giampaolo/psutil/actions/runs/15311348796/job/43076515731#step:5:3048
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bf660c09d150a8790e1b774338a7592666a584ba`.  There
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
{"case_id": "giampaolo_psutil__2580__bf660c0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
