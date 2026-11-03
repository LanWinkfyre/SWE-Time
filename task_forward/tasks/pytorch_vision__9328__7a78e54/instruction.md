# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
tv_tensors.wrap doesn't work with subclasses of BoundingBoxes or KeyPoints

### 🐛 Describe the bug

When using `tv_tensors.wrap` on an instance of a subclass of either `BoundingBoxes` or `KeyPoints` it will instead return the base class since they are hard-coded in. For example:

```python
from torchvision import tv_tensors

class MyKeyPoints(tv_tensors.KeyPoints):
    pass

kp = MyKeyPoints(torch.tensor([[0, 1], [2, 3]]), canvas_size=(4, 8))
```
```python
>>> kp
MyKeyPoints([[0, 1],
             [2, 3]], canvas_size=(4, 8))
>>> tv_tensors.wrap(kp, like=kp)
KeyPoints([[0, 1],
           [2, 3]], canvas_size=(4, 8))
```

### 🚀 Proposal

If instead of
```python
KeyPoints._wrap(wrappee, canvas_size=kwargs.get("canvas_size", like.canvas_size))
```
it was changed to
```python
type(like)._wrap(wrappee, canvas_size=kwargs.get("canvas_size", like.canvas_size))
```
then the subclass can be propagated. I see a possible downside to this where subclasses maybe don't support the exact same `kwargs` (e.g. `canvas_size` for `KeyPoints`) however it seems preferable to explicitly fail in that case and force a different approach vs. the potentially silent errors caused currently when the return type does not match the type of `like`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7a78e5419af9fe0edda5d9c952424defd1f8ffa7`.  There
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
{"case_id": "pytorch_vision__9328__7a78e54",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
