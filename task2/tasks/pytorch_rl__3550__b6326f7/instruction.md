# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] `SerialEnv` and `ParallelEnv` crash when placed on an MPS device

## Describe the bug

`SerialEnv` and `ParallelEnv` crash with a `TypeError` when placed on an MPS device (`device="mps"`) and the sub-environments emit `float64` observations. MPS does not support 64-bit floating-point, so any attempt to transfer a `float64` tensor to MPS raises:
```
TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.
```
Note that #3549 fixed the construction of the environment (by downcasting when the spec is created). But apparently this was not enough, as there are plenty of other places in the envs where tensors are cast to the parent device.

## To Reproduce

```python
import torch
from torchrl.envs import GymEnv, SerialEnv
env = SerialEnv(2, lambda: GymEnv("HalfCheetah-v4"), device="mps")
env.reset()
```

gives
```sh
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/common.py", line 3001, in reset
    tensordict_reset = self._reset(tensordict, **kwargs)
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/batched_envs.py", line 72, in decorated_fun
    return fun(self, *args, **kwargs)
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/batched_envs.py", line 1254, in _reset
    out = self.shared_tensordict_parent.named_apply(
  File "/Users/bensprenger/micromamba/envs/torchrl/lib/python3.10/site-packages/tensordict/base.py", line 9544, in named_apply
    result = self._apply_nest(
  File "/Users/bensprenger/micromamba/envs/torchrl/lib/python3.10/site-packages/tensordict/_td.py", line 1501, in _apply_nest
    item_trsf = fn(
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/batched_envs.py", line 1255, in <lambda>
    lambda *args: self.select_and_clone(
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/batched_envs.py", line 554, in select_and_clone
    return tensor.to(self.device, non_blocking=self.non_blocking)
TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.
```

## Expected behavior

It should be allowed to make a parent `ParallelEnv` on mps, even if the worker envs are on CPU and produce float64s. I think it should automatically downcast when the parent processes tensors from the workers.

## System info

* Installed from source
* MacOS Tahoe with MPS

```sh
>>> import torchrl, numpy, sys
>>> print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
0.10.0 2.2.6 3.10.18 | packaged by conda-forge | (main, Jun  4 2025, 14:46:00) [Clang 18.1.8 ] darwin
```

## Additional context

## Reason and Possible fixes

Primarily this is caused by casts from the workers' tensors to the parent's device without any guards for mismatch in dtype.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b6326f7726429241a66c888c4d70d588049f77a9`.  There
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
{"case_id": "pytorch_rl__3550__b6326f7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
