# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MultiCollector zeroes parameters/buffers of ClipPPOLoss when initialized with GPU modules on Windows

## Description

When initializing a MultiCollector, some internal values of modules that reference the actor/critic are unexpectedly reset to zero. This only happens if the actor, critic, and the modules (ClipPPOLoss, GAE) are already on the GPU before creating the MultiCollector.

I was able to reproduce this consistently on Windows 11, but I could not reproduce it on Linux.


## Expected behavior

Initializing a MultiCollector should not modify the state of existing modules such as ClipPPOLoss or GAE.

## Observed behavior

<img width="417" height="154" alt="Image" src="https://github.com/user-attachments/assets/f88464c8-1a01-4618-b901-6993726ccf7a" />

## Workaround

A workaround is to initialize MultiCollector first, and only afterwards either:

create the ClipPPOLoss/GAE, or
move them to the GPU.

This avoids the issue, although I could not find any documentation mentioning this requirement.

## To Reproduce

```python
import torchrl
from torchrl.modules import MLP, ValueOperator, TanhNormal
from torchrl.modules.tensordict_module import ProbabilisticActor
from torchrl.objectives import ClipPPOLoss
from torchrl.objectives.value import GAE
from torchrl.collectors import MultiCollector

import tensordict
from tensordict.nn import TensorDictModule, TensorDictSequential, NormalParamExtractor, TensorDictModuleBase

import torch

from torchrl.envs import GymEnv

from functools import partial

import torch.multiprocessing as mp



if __name__ == "__main__":


    env_factory = partial(GymEnv,"Pendulum-v1")

    device = 'cuda'
    nb_env = 4

    actor = ProbabilisticActor(
        module=TensorDictSequential(
            TensorDictModule(
                MLP(in_features=3, out_features=128, depth=2, num_cells=32),
                in_keys=["observation"],
                out_keys=["embedding"],
            ),
            TensorDictModule(
                MLP(in_features=128, out_features=2, depth=2, num_cells=32),
                in_keys=['embedding'],
                out_keys=['params'],
            ),
            TensorDictModule(
                NormalParamExtractor(),
                in_keys=['params'],
                out_keys=['loc', 'scale'],
            ),
        ),
        in_keys=['loc', 'scale'],
        distribution_class=TanhNormal,
        distribution_kwargs={'low': -2.0, 'high': 2.0},
        return_log_prob=True,
        cache_dist=True,
    )


    critic = ValueOperator(
        module=TensorDictSequential(
            TensorDictModule(MLP(in_features=3, out_features=128, depth=2, num_cells=32), in_keys=["observation"], out_keys=["embedding"]),
            MLP(in_features=128, out_features=1, depth=2, num_cells=32) 
        ),
        in_keys=["observation"],
    )

    loss = ClipPPOLoss(
            actor_network=actor,
            critic_network=critic,
            clip_epsilon=0.2,
            entropy_bonus=True,
            entropy_coeff=1e-3,
            critic_coeff=1.0,
            loss_critic_type="smooth_l1",
            normalize_advantage=True,
        )

    advantage = GAE(
            gamma=0.99,
            lmbda=0.95,
            value_network=critic,
            average_gae=True,
        )

    advantage = advantage.to(device)
    loss = loss.to(device)
    actor = actor.to(device)
    critic = critic.to(device)


    print('Before collector :')
    print('     loss clip epsilon =', loss.clip_epsilon)
    print('     advantage gamma =', advantage.gamma)   

    collector = MultiCollector(
        create_env_fn=[env_factory] * nb_env,
        sync=True,
        policy = actor,
        frames_per_batch=nb_env*10,
        total_frames=10000,
        policy_device=device,
        storing_device="cpu",
        env_device= 'cpu',
    )

    #advantage = advantage.to(device)
    #loss = loss.to(device)

    print('After collector :')
    print('     loss clip epsilon =', loss.clip_epsilon)
    print('     advantage gamma =', advantage.gamma)   


    collector.shutdown()
```


## System info

OS: Windows 11
PyTorch: 2.12.0+cu126
TorchRL: 0.13.2
TensorDict: 0.13.0
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f2a233715c54a6af875af93571ce9c5fbfd70d58`.  There
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
{"case_id": "pytorch_rl__3985__f2a2337",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
