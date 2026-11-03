# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
ops.masks_to_boxes , RuntimeError: min(): Expected reduction dim to be specified for input.numel() == 0. Specify the reduction dim with the 'dim' argument.

### 🐛 Describe the bug

The function ops.masks_to_boxes can't deal masks with one or more zero matrix. 

My simple solution:

`
for index, mask in enumerate(masks):
        y, x = torch.where(mask != 0)

        if y.numel() == 0 or x.numel() == 0:
            bounding_boxes[index, :] = 0
        else:
            bounding_boxes[index, 0] = torch.min(x)
            bounding_boxes[index, 1] = torch.min(y)
            bounding_boxes[index, 2] = torch.max(x)
            bounding_boxes[index, 3] = torch.max(y)
`

### Versions

0.22.0 and upper
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `df421b423f714eb3ae22cab2b0e6e7a6f6bb29be`.  There
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
{"case_id": "pytorch_vision__9346__df421b4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
