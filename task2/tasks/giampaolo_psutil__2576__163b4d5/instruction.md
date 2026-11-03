# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Use multi-phase initialisation (PEP 489)

## Summary

- OS: N/A (all)
- Type: core

## Description

Hello,

Please consider adopting multi-phase init for your Python extension modules. In short, multi-phase makes extension modules behave more like pure-Python modules and means that the import system can determine what a capabilities a module has before executing it.

Multi-phase initialisation was introduced in [PEP 489](https://peps.python.org/pep-0489/) for Python 3.5. It replaces the previous 'single-phase' mechanism by splitting the module creation process into creation and execution phases. Quoting from [the documentation](https://docs.python.org/3/c-api/module.html#multi-phase-initialization):

> Extension modules created this way behave more like Python modules: the initialization is split between the creation phase, when the module object is created, and the execution phase, when it is populated. The distinction is similar to the `__new__()` and `__init__()` methods of classes.

It is the preferred mechanism for extension module initialisation, and there is a proposal to [deprecate](https://discuss.python.org/t/89262/45) single phase init.

Thanks,
Adam

relates to #2565, as this would avoid using Unstable C API.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `163b4d5577281c4575c7fe7dc6d4fca542b37c7f`.  There
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
{"case_id": "giampaolo_psutil__2576__163b4d5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
