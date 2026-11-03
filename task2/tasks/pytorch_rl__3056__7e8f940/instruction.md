# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Cannot load serialized replay buffer with prioritized sampler from disk

## Describe the bug

After #3053, I was able to write a replay buffer to disk, and after #3055, I was able to also have a prioritized sampler in the replay buffer that I serialized. However, now I cannot *load* the replay buffer from disk. Note that loading works if I *don't* have a prioritized sampler, i.e commenting the `sampler=PrioritizedSampler(...)` line below makes the script work.

## To Reproduce

With this script

```python
from pathlib import Path
import tempfile

from tensordict import TensorDict
import torch
from torchrl.data import (
    LazyMemmapStorage,
    LazyTensorStorage,
    PrioritizedSampler,
    ReplayBuffer,
    TensorDictReplayBuffer,
)


def create_replay_buffer():
    return TensorDictReplayBuffer(
        storage=LazyTensorStorage(size, device=torch.device("cpu")),
        sampler=PrioritizedSampler(
            max_capacity=size,
            alpha=0.6,
            beta=0.4,
        ),
        batch_size=12,
        priority_key="td_error",
    )


size = 100

data = TensorDict(
    {
        "a": torch.ones(24, 2),
    },
    batch_size=[24],
)
replay_buffer = create_replay_buffer()
replay_buffer.extend(data)
print("rb extended")
sample = replay_buffer.sample()
print("sampled")
sample["td_error"] = torch.ones(12)
replay_buffer.update_tensordict_priority(sample)
print("priorities updated")
replay_buffer.dumps(Path("tmp"))
print("rb dumped")
del replay_buffer
new_replay_buffer = create_replay_buffer()
new_replay_buffer.loads(Path("tmp"))
print("rb loaded")

```
and the packages
```
cloudpickle==3.1.1
filelock==3.18.0
fsspec==2025.5.1
importlib-metadata==8.7.0
jinja2==3.1.6
markupsafe==3.0.2
mpmath==1.3.0
networkx==3.5
numpy==2.3.1
nvidia-cublas-cu12==12.6.4.1
nvidia-cuda-cupti-cu12==12.6.80
nvidia-cuda-nvrtc-cu12==12.6.77
nvidia-cuda-runtime-cu12==12.6.77
nvidia-cudnn-cu12==9.5.1.17
nvidia-cufft-cu12==11.3.0.4
nvidia-cufile-cu12==1.11.1.6
nvidia-curand-cu12==10.3.7.77
nvidia-cusolver-cu12==11.7.1.2
nvidia-cusparse-cu12==12.5.4.2
nvidia-cusparselt-cu12==0.6.3
nvidia-nccl-cu12==2.26.2
nvidia-nvjitlink-cu12==12.6.85
nvidia-nvtx-cu12==12.6.77
orjson==3.10.18
packaging==25.0
setuptools==80.9.0
sympy==1.14.0
tensordict==0.9.0
torch==2.7.1
torchrl==0.9.0
triton==3.3.1
typing-extensions==4.14.1
zipp==3.23.0
```
I get the error
```bash
rb extended
sampled
priorities updated
rb dumped
Traceback (most recent call last):
  File "/home/valter/Documents/Projects/rl-issues/scripts/replay_buffer.py", line 48, in <module>
    new_replay_buffer.loads(Path("tmp"))
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/valter/Documents/Projects/rl-issues/.venv/lib/python3.13/site-packages/torchrl/data/replay_buffers/replay_buffers.py", line 650, in loads
    self._sampler.loads(path / "sampler")
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/valter/Documents/Projects/rl-issues/.venv/lib/python3.13/site-packages/torchrl/data/replay_buffers/samplers.py", line 741, in loads
    tree_map(
    ~~~~~~~~^
        lambda dest, orig: dest.copy_(orig),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        tuple(self._max_priority),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
        tuple(metadata["_max_priority"]),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/valter/Documents/Projects/rl-issues/.venv/lib/python3.13/site-packages/torch/utils/_pytree.py", line 1145, in tree_map
    return treespec.unflatten(map(func, *flat_args))
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valter/Documents/Projects/rl-issues/.venv/lib/python3.13/site-packages/torch/utils/_pytree.py", line 982, in unflatten
    leaves = list(leaves)
  File "/home/valter/Documents/Projects/rl-issues/.venv/lib/python3.13/site-packages/torchrl/data/replay_buffers/samplers.py", line 742, in <lambda>
    lambda dest, orig: dest.copy_(orig),
                       ^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'copy_'
```

## Expected behavior

No error.

## System info

Fresh virtual environment, `pip install torchrl orjson`.

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```
outputs
```
0.9.0 2.3.1 3.13.3 (main, Apr  9 2025, 04:03:52) [Clang 20.1.0 ] linux
```

## Reason and Possible fixes

It has something to do with `PrioritizedSampler`, maybe the priorities? However, removing or adding `update_tensordict_priorities` in the script does not seem to change anything.

## Checklist

- [X] I have checked that there is no similar issue in the repo (**required**)
- [X] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [X] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7e8f9402f9108bc012944431c52557b2b93197cf`.  There
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
{"case_id": "pytorch_rl__3056__7e8f940",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
