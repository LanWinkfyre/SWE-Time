# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[illumos] zombie have no ctime

## Summary

- OS: illumos
- Architecture: 64bit
- Psutil version: 7.0.0
- Python version: 3.9.23
- Type: core
## Description

illumos (and presumably Solaris too) does have the exactly same problem with zombie processes as we saw with OpenBSD and NetBSD in #2287.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6a99365b73950e6c9a8d2dade55a1a90aa5c450e`.  There
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
{"case_id": "giampaolo_psutil__2593__6a99365",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
