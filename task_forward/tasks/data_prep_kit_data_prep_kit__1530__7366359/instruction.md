# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Bug] The new image transforms need to download the model libraries at run-time

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

transdforms/Other

### What happened + What you expected to happen

At the moment, the 3 model files needed by the image transforms are downloaded a priory into a `models `subfolder. This won't work when using these transforms by pip installing them in a notebook. Instead, a new model_type (yolo) in model_loader should be added and these models should be downloaded at run-time. 

### Reproduction script

1) pip install any of the 3 image transforms in a notebook
2) Using them results in a `model not found` error. 

### Anything else

See above. 

### OS

MacOS

### Python

3.12

### Are you willing to submit a PR?

- [ ] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `736635906a1a0ea926c2197ba8c4e6040326af6c`.  There
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
{"case_id": "data_prep_kit_data_prep_kit__1530__7366359",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
