# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
Add the `ABC` class as a base class to all transformers

Currently, `AbstractTransform` is the base class of all transforms and is defined as an Abstract class. However, nothing prevents its instantiation. 
The `transform_binary` method from `AbstractBinaryTransform` throws the `NotImplemented` exception. 

Python provides a more effective mechanism for defining abstract classes and methods by utilizing the `abc` Python Standard Library.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2ddef77abd5d0ae970cc51a8d42aef5629f004b2`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `dev`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "data_prep_kit_data_prep_kit__1382__2ddef77",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
