# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Linux] `Process.create_time()` does not reflect system clock updates

## Summary

* OS: Linux
* Type: core

## Description
As described by @kohlerjl in https://github.com/giampaolo/psutil/pull/2527, `Process.create_time()` on Linux is not updated if system clock time is updated. The reason is because we used a cached result from `psutil.boot_time()`. 

It turns out we have the same problem on macOS (#2570), even if for different reasons.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fa71912e600e9b439274b392741ac797085363f9`.  There
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
{"case_id": "giampaolo_psutil__2541__fa71912",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
