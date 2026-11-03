# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
Incorrect BoundingBoxes format conversion  CXCYWH -> XYXY

Thanks to @antoinesimoulin for uncovering this issue in https://github.com/pytorch/vision/pull/8841/commits/5321f234fdac29fa3c1c708dfdeeb9e0b1ae5e0a


```python
old_format = tv_tensors.BoundingBoxFormat.CXCYWH
new_format = tv_tensors.BoundingBoxFormat.XYXY

dtype = torch.int64
fn_type = "functional"
device = torch.device("cpu")


# bounding_boxes = make_bounding_boxes(format=old_format, dtype=dtype, device=device)
bounding_boxes = tv_tensors.BoundingBoxes([[ 5,  6, 10, 13]], format=tv_tensors.BoundingBoxFormat.CXCYWH, canvas_size=(17, 11))

if fn_type == "functional":
    fn = functools.partial(F.convert_bounding_box_format, new_format=new_format)
else:
    fn = transforms.ConvertBoundingBoxFormat(format=new_format)

actual = fn(bounding_boxes)
expected = _reference_convert_bounding_box_format(bounding_boxes, new_format)

assert_equal(actual, expected)
```

Gives:

```
BoundingBoxes([[ 0, -1, 10, 12]], format=BoundingBoxFormat.XYXY, canvas_size=(17, 11))
BoundingBoxes([[ 0,  0, 10, 12]], format=BoundingBoxFormat.XYXY, canvas_size=(17, 11))
```

The `-1` part is clearly wrong. Maybe an easy fix is to call `max(0, ...)` at some point but I haven't looked into it yet.


cc @vfdev-5
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6940e19087cecb5108370703e207f7a33d9b478d`.  There
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
{"case_id": "pytorch_vision__8887__6940e19",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
