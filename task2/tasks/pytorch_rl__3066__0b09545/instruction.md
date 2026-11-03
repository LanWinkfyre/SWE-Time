# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Data collection error on M1 Macs

## Describe the bug

SyncDataCollector RuntimeError on Mac-M1 when using `mps` device. 



## To Reproduce
```python
from pettingzoo.butterfly import pistonball_v6
from torchrl.collectors import SyncDataCollector
from torchrl.envs import ParallelEnv
from torchrl.envs.libs.pettingzoo import PettingZooWrapper


DEVICE = "mps"

kwargs = {"n_pistons": 21, "continuous": True}
inner_env_fn = lambda: PettingZooWrapper(
    env=pistonball_v6.parallel_env(**kwargs),
    return_state=True,
    group_map=None,
    device=DEVICE,
)
collector_env = lambda: ParallelEnv(num_workers=2, create_env_fn=inner_env_fn)
collector = SyncDataCollector(collector_env, frames_per_batch=100)

collector.reset()
print(next(iter(collector)))
collector.shutdown()
```
```bash
  File ".../.venv/lib/python3.11/site-packages/torch/storage.py", line 447, in wrapper
    return fn(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../.venv/lib/python3.11/site-packages/torch/storage.py", line 526, in _share_filename_cpu_
    return super()._share_filename_cpu_(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: _share_filename_: only available on CPU
```


## Expected behavior
Should be able to create env on mps and collect data. 

## Screenshots

If applicable, add screenshots to help explain your problem.

## System info

```
>>> print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
0.8.0+83cb41d 2.0.2 3.11.8 (main, Feb 25 2024, 03:55:37) [Clang 17.0.6 ] darwin
```
```
>>> platform.platform()
'macOS-15.5-arm64-arm-64bit'
```

Running via `uv`


## Additional context

- No issue when collecting directly on cpu or cuda 
- No issue when using SerialEnv over ParallelEnv

## Reason and Possible fixes

Seems related to https://github.com/pytorch/pytorch/issues/87688

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0b095459dc500d8f8952cd02ea9b47729d08f6c8`.  There
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
{"case_id": "pytorch_rl__3066__0b09545",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
