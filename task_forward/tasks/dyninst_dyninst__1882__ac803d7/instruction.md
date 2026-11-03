# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
unable to parse MI300A GPU binary

**Intention**
HPCToolkit's hpcstruct had a problem parsing an MI300A GPU binary with Dyninst master

**Describe the bug**
Rose instruction semantics came across a bad register

**To Reproduce**
Try to parse the attached binary with dyninst master

**Expected behavior**
I don't expect Rose instruction semantics to crash

**System (please complete the following information):**
x86_64
master


**Additional context**
Add any other context about the problem here.

[1213c84c567e3c4db3f5e603ffa4a51e.gpubin.gz](https://github.com/user-attachments/files/18553922/1213c84c567e3c4db3f5e603ffa4a51e.gpubin.gz)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ac803d7af626455abaa3bbd69ea997fd6099a371`.  There
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
{"case_id": "dyninst_dyninst__1882__ac803d7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
