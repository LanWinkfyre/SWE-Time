# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Questions about ReplayBuffers

## Motivation

I have a few questions regarding the use of ReplayBuffers. I wasnt able to find answers in any of the existing docs, so happy to put up changes if the info would be useful to others. 

- What should be the dimensions of the tensordicts provided to ReplayBuffer.add vs ReplayBuffer.extend? I understand add is for "single element" and extend is for "a sequence of elements", but how do you define elements with batched tensors?
- What is the correct way of using SyncDataCollectors and SliceSamplers to sample trajectories from the replay buffer? Both the following methods work, but wasn't sure which is preferred. Also in both methods I have to manually reshape tensors to get them in the form of (*B, T). Is this expected?


Snippet 1. 
(Adapted from https://github.com/pytorch/rl/blob/7874e74cb8f00b736f6ee0a8fbddb252c99de6fa/docs/source/reference/collectors.rst#collectors-and-replay-buffers-interoperability)
```
from torchrl.collectors import SyncDataCollector
from torchrl.data import TensorDictReplayBuffer
from torchrl.data.replay_buffers.samplers import SliceSampler
from torchrl.data.replay_buffers.storages import LazyTensorStorage
from torchrl.envs.libs.vmas import VmasEnv

NUM_ENVS = 2
BUFFER_SIZE = 10000
DEVICE = "cpu"
TOTAL_FRAMES = 1000
MAX_STEPS = 50
SEQ_LEN = 10
MINIBATCH_SIZE = 50

num_slices = MINIBATCH_SIZE // SEQ_LEN

env = VmasEnv(
    scenario="give_way",
    num_envs=NUM_ENVS,
    continuous_actions=False,
    max_steps=MAX_STEPS,
)

sampler = SliceSampler(
    num_slices=num_slices,
    traj_key=("collector", "traj_ids"),
    strict_length=True,
)
buffer = TensorDictReplayBuffer(
    storage=LazyTensorStorage(
        BUFFER_SIZE, device="cpu", ndim=2 
    ), 
    sampler=sampler,
)
collector = SyncDataCollector(
    env,
    device=DEVICE,
    storing_device=DEVICE,
    frames_per_batch=TOTAL_FRAMES,
    total_frames=TOTAL_FRAMES,
)

data = next(iter(collector))  # (n_envs, time)

buffer.extend(data)  # Adding unflattened data

sample = buffer.sample(MINIBATCH_SIZE)  # Size (T,), multiple slices stacked

sample = sample.reshape(sample.shape[0] // SEQ_LEN, SEQ_LEN)  # Size (B, T)
```


Snippet 2
```
from torchrl.collectors import SyncDataCollector
from torchrl.data import TensorDictReplayBuffer
from torchrl.data.replay_buffers.samplers import SliceSampler
from torchrl.data.replay_buffers.storages import LazyTensorStorage
from torchrl.envs.libs.vmas import VmasEnv

NUM_ENVS = 2
BUFFER_SIZE = 1000
DEVICE = "cpu"
TOTAL_FRAMES = 1000
MAX_STEPS = 50
SEQ_LEN = 10
MINIBATCH_SIZE = 50

num_slices = MINIBATCH_SIZE // SEQ_LEN

env = VmasEnv(
    scenario="give_way",
    num_envs=NUM_ENVS,
    continuous_actions=False,
    max_steps=MAX_STEPS,
)
sampler = SliceSampler(
    num_slices=num_slices,
    traj_key=("collector", "traj_ids"),
    strict_length=True,
)
buffer = TensorDictReplayBuffer(
    storage=LazyTensorStorage(
        BUFFER_SIZE,
        device="cpu",
    ),
    sampler=sampler,
)
collector = SyncDataCollector(
    env,
    device=DEVICE,
    storing_device=DEVICE,
    frames_per_batch=TOTAL_FRAMES,
    total_frames=TOTAL_FRAMES,
)

data = next(iter(collector))  # (n_envs, time)

buffer.extend(data.reshape(-1))  # Adding flattened data

sample = buffer.sample(MINIBATCH_SIZE)  # Size (T,), multiple slices stacked

sample = sample.reshape(sample.shape[0] // SEQ_LEN, SEQ_LEN)  # Size (B, T)
```




## Solution

Documentation changes

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f7592c667b8ed05567fc2e05564b01c73347051d`.  There
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
{"case_id": "pytorch_rl__3146__f7592c6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
