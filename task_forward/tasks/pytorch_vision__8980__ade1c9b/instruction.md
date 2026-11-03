# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
nvjpeg missing from all linux GPU wheel build jobs

Linux CUDA: https://github.com/pytorch/vision/actions/runs/13901104094/job/38892841516?pr=8601
Linux aarch64 CUDA: https://github.com/pytorch/vision/actions/runs/13901104115/job/38892844332?pr=8601

Failing the smoke test part with:

```
+ echo 'pytorch/vision/test/smoke_test.py found'
+ conda run -p /__w/_temp/conda_environment_13901104115 python pytorch/vision/test/smoke_test.py
/__w/_temp/conda_environment_13901104115/lib/python3.9/site-packages/torchvision/io/image.py:14: UserWarning: Failed to load image Python extension: 'libnvjpeg.so.12: cannot open shared object file: No such file or directory'If you don't plan on using image functionality from `torchvision.io`, you can ignore this warning. Otherwise, there might be something wrong with your environment. Did you have `libjpeg` or `libpng` installed before building `torchvision` from source?

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ade1c9bed1014d7ef3539d859d5656f5d091407e`.  There
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
{"case_id": "pytorch_vision__8980__ade1c9b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
