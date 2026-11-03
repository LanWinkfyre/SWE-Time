# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] QValueActor does not respect action_spec

## Describe the bug

When QValueActor is used with an action spec that has a singleton dimension (1,) for the action, the action shape instead becomes ().

## To Reproduce

```python
from tensordict import TensorDict
from tensordict.nn import TensorDictModule
from torch import nn
import torch
from torchrl.modules.tensordict_module import QValueActor
from torchrl.data import Categorical

action_spec = Categorical(4, shape=torch.Size((1, 1)), dtype=torch.int64)

module = TensorDictModule(
    module=nn.Linear(3, 1), in_keys=("observation"), out_keys=("action_value")
)

qvalue_actor = QValueActor(
    module=module,
    in_keys=["observation"],
    spec=action_spec,
)

td = TensorDict({"observation": torch.randn(12, 3)})
qvalue_actor(td)
print(td)
```

```bash
TensorDict(
    fields={
        action: Tensor(shape=torch.Size([12]), device=cpu, dtype=torch.int64, is_shared=False),
        action_value: Tensor(shape=torch.Size([12, 1]), device=cpu, dtype=torch.float32, is_shared=False),
        chosen_action_value: Tensor(shape=torch.Size([12, 1]), device=cpu, dtype=torch.float32, is_shared=False),
        observation: Tensor(shape=torch.Size([12, 3]), device=cpu, dtype=torch.float32, is_shared=False)},
    batch_size=torch.Size([]),
    device=None,
    is_shared=False)
```

## Expected behavior

`action.shape` should be `torch.Size([12, 1])`

## System info

Packages:
```
asttokens==3.0.0
cloudpickle==3.1.1
decorator==5.2.1
executing==2.2.0
filelock==3.18.0
fsspec==2025.5.1
importlib-metadata==8.7.0
ipython==9.4.0
ipython-pygments-lexers==1.1.1
jedi==0.19.2
jinja2==3.1.6
markupsafe==3.0.2
matplotlib-inline==0.1.7
mpmath==1.3.0
networkx==3.5
numpy==2.3.1
nvidia-cublas-cu12==12.4.5.8
nvidia-cuda-cupti-cu12==12.4.127
nvidia-cuda-nvrtc-cu12==12.4.127
nvidia-cuda-runtime-cu12==12.4.127
nvidia-cudnn-cu12==9.1.0.70
nvidia-cufft-cu12==11.2.1.3
nvidia-curand-cu12==10.3.5.147
nvidia-cusolver-cu12==11.6.1.9
nvidia-cusparse-cu12==12.3.1.170
nvidia-cusparselt-cu12==0.6.2
nvidia-nccl-cu12==2.21.5
nvidia-nvjitlink-cu12==12.4.127
nvidia-nvtx-cu12==12.4.127
orjson==3.10.18
packaging==25.0
parso==0.8.4
pexpect==4.9.0
prompt-toolkit==3.0.51
ptyprocess==0.7.0
pure-eval==0.2.3
pygments==2.19.2
stack-data==0.6.3
sympy==1.13.1
tensordict==0.8.3
torch==2.6.0
torchrl==0.7.2
traitlets==5.14.3
triton==3.2.0
typing-extensions==4.14.1
wcwidth==0.2.13
zipp==3.23.0
```

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```
outputs
```
0.7.2 2.3.1 3.11.9 (main, Aug 14 2024, 05:07:28) [Clang 18.1.8 ] linux
```

## Additional context

This problem could of course be avoided by simply removing the last dimension, but I like the idea of letting all tensors in the tensordict have the same number of dimensions. This makes it easier to reason about dimensions once you start adding batches and multiple agents.

## Reason and Possible fixes

No clue.

## Checklist

- [X] I have checked that there is no similar issue in the repo (**required**)
- [X] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [X] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bb1c1680525d380824af033d64e3ce84f71836ae`.  There
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
{"case_id": "pytorch_rl__3059__bb1c168",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
