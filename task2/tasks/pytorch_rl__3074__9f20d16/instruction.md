# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Binary tensor spec is not compatible with `shape=()`

## Describe the bug

 https://github.com/pytorch/rl/pull/2979 introduced the possibility of passing a `shape = ()` to the `Binary` spec to model scalar binary values. However the `Binary.clone()` method has not been updated to be compatible as well.

The same can be said regarding other methods, such as `._unsqeeze()`

## To Reproduce

```python
import pytest
from torchrl.data import Binary


def test__Binary__can_handle_empty_spec() -> None:
    with pytest.raises(IndexError, match="tuple index out of range"):
        Binary(shape=()).clone()
```


## Reason and Possible fixes

The main problem is that whenever the Binary operates on itself, it returns a `self.__class__(n=self.shape[-1], shape=shape, ... )`, which fails when `shape=()` due to `self.shape[-1]`.

I would suggest to replace all `n=self.shape[-1]` occurrences with `n=self.n` when the shape is unchanged (eg, in the `.clone()`). Have not thought what to do for the other cases such as `._unsqueeze()`, but I am available for a PR and will think about this later.

## Checklist

- [X] I have checked that there is no similar issue in the repo
- [X] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) 
- [X] I have provided a minimal working example to reproduce the bug
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9f20d167707c27de57976a51bf75b8dfb8f092bc`.  There
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
{"case_id": "pytorch_rl__3074__9f20d16",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
