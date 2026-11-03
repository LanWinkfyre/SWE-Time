# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] `R3MTransform` is wrongly used in "USING PRETRAINED MODELS" tutorial

## Describe the bug

`R3MTransform` operated under `@torch.no_grad()` and thus cannot be trained contrary to what the tutorial is implying.

## To Reproduce

```python
import torch
from torch import nn
from torchrl.envs import R3MTransform, DTypeCastTransform, TransformedEnv
from torchrl.envs.libs.gym import GymEnv
from torchrl.modules import Actor
from tensordict.nn import TensorDictSequential


base_env = GymEnv("Ant-v4", from_pixels=True)
env = TransformedEnv(base_env, DTypeCastTransform(dtype_in=torch.uint8, dtype_out=torch.float32, in_keys=["pixels"]))

r3m = R3MTransform("resnet50", in_keys=["pixels"], download=True)
net = nn.Sequential(
    nn.LazyLinear(128),
    nn.Tanh(),
    nn.Linear(128, env.action_spec.shape[-1]),
)
actor = Actor(net, in_keys=["r3m_vec"])
r3m.train()
policy = TensorDictSequential(r3m, actor)
rollout = base_env.rollout(10)

output = policy(rollout)
init_grad = torch.ones_like(output["action"])

output["action"].backward(init_grad, retain_graph=True)
for name, param in policy[0].named_parameters():
    if param.grad is not None:
        print(name) # nothing printed (silent failure)

torch.autograd.grad(output["action"], net[2].weight, init_grad, retain_graph=True) # works as expected
torch.autograd.grad(output["action"], policy[0].transforms[3].convnet.conv1.weight, init_grad, retain_graph=True) # raises
```

## Expected behavior

I would have expected the transform to propagate gradients when not used as an environment transform (only).

## Screenshots

NA

## System info

Describe the characteristic of your environment:
 * torchrl v0.9.2
 * Python v3.10.11

## Additional context

`R3M` also has other issues like wrong type hints and non-optional delete keys.

## Reason and Possible fixes

Maybe create an `R3MModule` (from `TensorDictModule`) that could be used in the corresponding transform or in a policy as a feature extractor.

Maybe native support for (pretrained) feature extractor could be a nice to have in the modules, beyond transforms, e.g. like in SB3.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a5cc95fc587fd3c0bb8b64df91ed41c219b6bebf`.  There
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
{"case_id": "pytorch_rl__3131__a5cc95f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
