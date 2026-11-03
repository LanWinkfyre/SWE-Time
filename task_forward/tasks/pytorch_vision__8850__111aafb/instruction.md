# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
The doc of `CocoDetection()` and `CocoCaptions()` should say "You must install `pycocotools`."

### 📚 The doc issue

The doc of [CocoDetection()](https://pytorch.org/vision/stable/generated/torchvision.datasets.CocoDetection.html) and [CocoCaptions()](https://pytorch.org/vision/stable/generated/torchvision.datasets.CocoCaptions.html) says below:

> It requires the [COCO API to be installed](https://github.com/pdollar/coco/tree/master/PythonAPI).

But [COCO API](https://github.com/pdollar/coco/tree/master/PythonAPI) doesn't work because it's outdated.

### Suggest a potential alternative/fix

So, the doc should say as shown below:

> You must install `pycocotools`, e.g. `pip install pycocotools`, `conda install conda-forge::pycocotools`, etc. *Don't use [COCO API](https://github.com/pdollar/coco/tree/master/PythonAPI) because it doesn't work because it's outdated.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `111aafb659c14929fe7ff7a75fc0b9576dae4c75`.  There
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
{"case_id": "pytorch_vision__8850__111aafb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
