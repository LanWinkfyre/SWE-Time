# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MPS device crashes on float64 specs when moving environments with .to('mps')

## Describe the bug

Creating a `SyncDataCollector` (or `Collector`) with `env_device="mps"` crashes with `TypeError: Cannot convert a MPS Tensor to float64 dtype` because gymnasium/MuJoCo environments produce float64 observation and action spaces, and MPS does not support float64 tensors.

## To Reproduce

On a Mac with MPS:
```python
import torch
from torchrl.envs import GymEnv
from torchrl.collectors import SyncDataCollector

env = GymEnv("HalfCheetah-v4")

collector = SyncDataCollector(
    env,
    policy=env.rand_action,
    frames_per_batch=10,
    total_frames=10,
    device="mps",
    env_device="mps",
)
```

```sh
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bensprenger/repositories/torchRL/torchrl/collectors/_base.py", line 1050, in __call__
    return super().__call__(*args, **kwargs)
  File "/Users/bensprenger/repositories/torchRL/torchrl/collectors/_single.py", line 519, in __init__
    self._apply_env_device()
  File "/Users/bensprenger/repositories/torchRL/torchrl/collectors/_single.py", line 872, in _apply_env_device
    self.env: EnvBase = self.env.to(self.env_device)
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/common.py", line 76, in wrapper
    result = func(self, *args, **kwargs)
  File "/Users/bensprenger/repositories/torchRL/torchrl/envs/common.py", line 4001, in to
    self.__dict__["_output_spec"] = self.output_spec.to(device)
  File "/Users/bensprenger/repositories/torchRL/torchrl/data/tensor_specs.py", line 5962, in to
    kwargs[key] = value.to(dest)
  File "/Users/bensprenger/repositories/torchRL/torchrl/data/tensor_specs.py", line 5962, in to
    kwargs[key] = value.to(dest)
  File "/Users/bensprenger/repositories/torchRL/torchrl/data/tensor_specs.py", line 3165, in to
    return Unbounded(shape=self.shape, device=dest_device, dtype=dest_dtype)
  File "/Users/bensprenger/repositories/torchRL/torchrl/data/tensor_specs.py", line 3034, in __call__
    instance = super().__call__(*args, **kwargs)
  File "/Users/bensprenger/repositories/torchRL/torchrl/data/tensor_specs.py", line 3130, in __init__
    torch.full(
TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.
```

## Expected behavior

A clear and concise description of what you expected to happen.

## Screenshots

## System info

 * Installed from source in a micromamba environment
 * macOS (Apple Silicon M-series)
 * Python version 3.10

```python
>>> import torchrl, numpy, sys
>>> print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
0.10.0 2.2.6 3.10.18 | packaged by conda-forge | (main, Jun  4 2025, 14:46:00) [Clang 18.1.8 ] darwin
```

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1ed0d1e40f590420a123006affb958b4c02b0b8c`.  There
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
{"case_id": "pytorch_rl__3549__1ed0d1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
