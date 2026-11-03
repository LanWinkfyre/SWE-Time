# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MultiSyncDataCollector fails with set_seed and split_trajs=True

## Describe the bug

MultiSyncDataCollector throws an error when using set_seed and split_trajs=True.

## To Reproduce

```python
from torchrl.envs.libs.gym import GymEnv
from tensordict.nn import TensorDictModule
from torch import nn
from torchrl.collectors import MultiSyncDataCollector
if __name__ == "__main__":
    env_maker = lambda: GymEnv("Pendulum-v1", device="cpu")
    policy = TensorDictModule(nn.Linear(3, 1), in_keys=["observation"], out_keys=["action"])
    collector = MultiSyncDataCollector(
        create_env_fn=[env_maker, env_maker],
        policy=policy,
        total_frames=2000,
        max_frames_per_traj=50,
        frames_per_batch=200,
        init_random_frames=-1,
        reset_at_each_iter=False,
        device="cpu",
        storing_device="cpu",
        cat_results=0,
        split_trajs=True,
    )
    collector.set_seed(42)
    for i, data in enumerate(collector):
        if i == 2:
            print(data)
            break
    collector.shutdown()
    del collector
```

```bash
Traceback (most recent call last):
  File "<...>/multisyncdatacollector_seed_test.py", line 22, in <module>
    for i, data in enumerate(collector):
                   ^^^^^^^^^^^^^^^^^^^^
  File "<...>/lib/python3.12/site-packages/torchrl/collectors/collectors.py", line 342, in __iter__
    yield from self.iterator()
  File "<...>/lib/python3.12/site-packages/torchrl/collectors/collectors.py", line 3035, in iterator
    out = split_trajectories(self.out_buffer, prefix="collector")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<...>/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "<...>/lib/python3.12/site-packages/torchrl/collectors/utils.py", line 241, in split_trajectories
    out_splits = out_splits.split(splits, 0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<...>/lib/python3.12/site-packages/tensordict/_td.py", line 1780, in split
    splits = {k: v.split(split_size, dim) for k, v in self.items()}
                 ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<...>/lib/python3.12/site-packages/torch/_tensor.py", line 983, in split
    return torch._VF.split_with_sizes(self, split_size, dim)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: split_with_sizes expects split_sizes to sum exactly to 200 (input tensor's size at dimension 0), but got split_sizes=[100, 50, 100, 50]
  File ... 
```

## Expected behavior

Expect MultiSyncDataCollector iterator to return repeatable results based on the input seed set in .set_seed()

## Screenshots

N/A

## System info

Describe the characteristic of your environment:
 * Installed via mambaforge
 * Python version 3.12
 * TorchRL v0.10.0, Tensordict v0.10.0

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)>>> print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
0.0.0+unknown 2.3.4 3.12.12 | packaged by conda-forge | (main, Oct 22 2025, 23:34:53) [Clang 19.1.7 ] darwin
```

## Additional context

Works as expected in TorchRL v0.6.0. Have not checked other versions.

## Reason and Possible fixes

Temporary work-around is to set the environment seeds manually in the create_env_fn and sort the resulting data Tensordict. Sorting is apparently necessary because the data may be in a different order depending on when each process finishes.

## Checklist

- [ x ] I have checked that there is no similar issue in the repo (**required**)
- [ x ] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [ x ] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8da8433265b328aac9e631d7d9e22325b1f44364`.  There
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
{"case_id": "pytorch_rl__3238__8da8433",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
