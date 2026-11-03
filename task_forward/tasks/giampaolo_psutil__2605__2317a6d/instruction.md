# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Linux] sbattery.secsleft is negative

## `psutil.sensors_battery()` reports a negative amount for seconds left

- OS: ArchLinux
- Architecture: 64bit
- Psutil version: 7.0.0
- Python version: 3.13.5
- Type: core

## Description

```python
>>> import psutil
>>> psutil.sensors_battery()
sbattery(percent=65.32751091703057, secsleft=-7119, power_plugged=False)
```

The value for `secsleft` is negative instead of positive.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2317a6d254a83a9ee140b44e8ca86b01aef2dee0`.  There
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
{"case_id": "giampaolo_psutil__2605__2317a6d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
