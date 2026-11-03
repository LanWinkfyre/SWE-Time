# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[OS Independent] Reverse children in doc example "Kill process tree"

## Summary

* OS: Independent
* Type: doc

## Description

In the example [Kill process tree](https://psutil.readthedocs.io/en/latest/index.html#kill-process-tree), the children are killed in the order which is given by the function [psutil.Process.children](https://psutil.readthedocs.io/en/latest/index.html#psutil.Process.children). Related to the documentation the returned list contains the processes in top-down order.

But if there are grand children or great grandchildren, the parents of them are then killed before them, which seems incorrect. The child hierarchy should be killed in order lowest first, mean in a bottom-up approach.

Enhancing the 'Kill process tree' example in the way that reversing the given children list before killing the items should fix this.

```python
# Instead ...
children = parent.children(recursive=True)
# use ...
children = parent.children(recursive=True).reverse()
# or ...
children = list(reversed(parent.children(recursive=True)))
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a5b9e78927245781b71e7e065a515ebd06fe4908`.  There
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
{"case_id": "giampaolo_psutil__2573__a5b9e78",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
