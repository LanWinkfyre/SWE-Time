# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Replace node-disk-info library

### Paste the command

N/A

### Describe the bug

`node-disk-info` hasn't had an update in 4.5 years, and the author has stopped responding to GitHub issues.

It relies on the `wmic` command on Windows, which is going away: https://support.microsoft.com/en-us/topic/windows-management-instrumentation-command-line-wmic-removal-from-windows-e9e83c7f-4992-477f-ba1d-96f694b8665d

RE: https://github.com/cristiammercado/node-disk-info/issues/29

### Expected behavior

Igir should work on all modern OSes.

### Debug logs

N/A

### DAT(s) used

_No response_

### igir version

v4.2.0

### Node.js version

N/A

### Operating system

Windows

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `37c97de57d7de4388926a92d91bc237324e68295`.  There
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
{"case_id": "emmercm_igir__1883__37c97de",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
