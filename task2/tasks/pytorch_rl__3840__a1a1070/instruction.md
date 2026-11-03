# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MultiSyncCollector may perform unnecessary get(timeout=_TIMEOUT) calls after receiving all worker outputs

## Describe the bug

While profiling `MultiSyncCollector`, I observed a recurring idle delay during the worker output gathering phase.

In the minimal example below, with `num_workers=16`, the elapsed time is about 16 seconds when `preemptive_threshold=1.0`, even though the artificial environment step delay is only 1.1 seconds.

From the debug logs, the delay consists of:

* one initial timeout before any worker output becomes available
* `(num_workers - 1)` additional timeouts after all worker outputs have already been received

The second part appears to occur after all worker outputs have already been received and may be unnecessary.

The relevant code path is:

https://github.com/pytorch/rl/blob/main/torchrl/collectors/_multi_sync.py#L253-L263

```python
recv = collections.deque()
t0 = time.time()
while len(recv) < self.num_workers and (
    (time.time() - t0) < (_TIMEOUT * _MAX_IDLE_COUNT)
):
    for _ in range(self.num_workers):
        try:
            new_data, j = self.queue_out.get(timeout=_TIMEOUT)
            recv.append((new_data, j))
        except (TimeoutError, Empty):
            _check_for_faulty_process(self.procs)
```

## To Reproduce

The following minimal example reproduces the issue by inserting a sleep slightly longer than `_TIMEOUT=1.0` into each environment step.

```python
import time
import numpy as np
import torch
import torch.nn as nn
import gymnasium as gym

from gymnasium import spaces
from tensordict.nn import TensorDictModule
from torchrl.envs.libs.gym import GymWrapper
from torchrl.collectors import MultiSyncCollector


class SleepEnv(gym.Env):
    def __init__(self, sleep_time=1.1):
        super().__init__()
        self.sleep_time = sleep_time
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(1,),
            dtype=np.float32,
        )
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(1,),
            dtype=np.float32,
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        obs = np.zeros((1,), dtype=np.float32)
        return obs, {}

    def step(self, action):
        time.sleep(self.sleep_time)
        obs = np.zeros((1,), dtype=np.float32)
        reward = 0.0
        terminated = False
        truncated = False
        info = {}
        return obs, reward, terminated, truncated, info


class ZeroPolicy(nn.Module):
    def forward(self, observation):
        return torch.zeros(
            (*observation.shape[:-1], 1),
            dtype=observation.dtype,
            device=observation.device,
        )


def make_env():
    return GymWrapper(SleepEnv(sleep_time=1.1))


def run(preemptive_threshold):
    num_workers = 16

    policy = TensorDictModule(
        ZeroPolicy(),
        in_keys=["observation"],
        out_keys=["action"],
    )

    collector = MultiSyncCollector(
        create_env_fn=[make_env] * num_workers,
        policy=policy,
        frames_per_batch=num_workers,
        total_frames=num_workers,
        preemptive_threshold=preemptive_threshold,
        device="cpu",
        storing_device="cpu",
    )

    t0 = time.time()
    next(iter(collector))
    elapsed = time.time() - t0

    collector.shutdown()

    print(
        f"preemptive_threshold={preemptive_threshold}, "
        f"elapsed={elapsed:.3f}s"
    )


if __name__ == "__main__":
    run(preemptive_threshold=1.0)
    run(preemptive_threshold=0.99)
```

Observed output:

```text
preemptive_threshold=1.0, elapsed=16.170s
preemptive_threshold=0.99, elapsed=1.142s
```

I also inserted debug prints immediately before and after:

```python
new_data, j = self.queue_out.get(timeout=_TIMEOUT)
```

and printed when a timeout occurred.

The output was:

```text
before get: len(recv)=0, time.time()-t0=0.0000
timeout
before get: len(recv)=0, time.time()-t0=1.0012
after get
before get: len(recv)=1, time.time()-t0=1.1093
after get
before get: len(recv)=2, time.time()-t0=1.1108
after get
before get: len(recv)=3, time.time()-t0=1.1119
after get
before get: len(recv)=4, time.time()-t0=1.1144
after get
before get: len(recv)=5, time.time()-t0=1.1169
after get
before get: len(recv)=6, time.time()-t0=1.1192
after get
before get: len(recv)=7, time.time()-t0=1.1215
after get
before get: len(recv)=8, time.time()-t0=1.1371
after get
before get: len(recv)=9, time.time()-t0=1.1382
after get
before get: len(recv)=10, time.time()-t0=1.1393
after get
before get: len(recv)=11, time.time()-t0=1.1403
after get
before get: len(recv)=12, time.time()-t0=1.1415
after get
before get: len(recv)=13, time.time()-t0=1.1425
after get
before get: len(recv)=14, time.time()-t0=1.1438
after get
before get: len(recv)=15, time.time()-t0=1.1449
after get
before get: len(recv)=16, time.time()-t0=1.1459
timeout
before get: len(recv)=16, time.time()-t0=2.1471
timeout
before get: len(recv)=16, time.time()-t0=3.1485
timeout
before get: len(recv)=16, time.time()-t0=4.1491
timeout
before get: len(recv)=16, time.time()-t0=5.1505
timeout
before get: len(recv)=16, time.time()-t0=6.1514
timeout
before get: len(recv)=16, time.time()-t0=7.1529
timeout
before get: len(recv)=16, time.time()-t0=8.1545
timeout
before get: len(recv)=16, time.time()-t0=9.1560
timeout
before get: len(recv)=16, time.time()-t0=10.1576
timeout
before get: len(recv)=16, time.time()-t0=11.1582
timeout
before get: len(recv)=16, time.time()-t0=12.1593
timeout
before get: len(recv)=16, time.time()-t0=13.1608
timeout
before get: len(recv)=16, time.time()-t0=14.1623
timeout
before get: len(recv)=16, time.time()-t0=15.1637
timeout
```

## Expected behavior

Once `len(recv)` reaches `self.num_workers`, I would expect the collector to stop issuing additional:

```python
self.queue_out.get(timeout=_TIMEOUT)
```

calls.

No additional timeout delays should occur after all worker outputs have been received.

## Screenshots

N/A

## System info

Installed via pip.

Environment:

```text
OS: Linux
Python: 3.10.19
NumPy: 2.2.6
PyTorch: 2.9.1+cu128
Gymnasium: 1.2.2
TorchRL: 0.13.1
TensorDict: 0.13.0
```

## Additional context

The delay is not observed when using:

```python
preemptive_threshold = 0.99
```

In the minimal example above, the elapsed time changes from:

```text
preemptive_threshold=1.0  -> 16.170s
preemptive_threshold=0.99 -> 1.142s
```

The delay also disappears if the following early-exit condition is added to the inner loop:

```python
for _ in range(self.num_workers):
    if len(recv) >= self.num_workers:
        break

    try:
        new_data, j = self.queue_out.get(timeout=_TIMEOUT)
        recv.append((new_data, j))
    except (TimeoutError, Empty):
        _check_for_faulty_process(self.procs)
```

## Reason and Possible fixes

My current hypothesis is that the interaction between:

* the initial timeout,
* the outer `while` loop,
* and the fixed-length inner `for` loop

can cause unnecessary `get(timeout=_TIMEOUT)` calls after all worker outputs have already been received.

In the example above:

1. The first `get(timeout=_TIMEOUT)` times out because no worker output is available within the first `_TIMEOUT` seconds.
2. Worker outputs are then received rapidly.
3. `len(recv)` reaches `self.num_workers` during the inner `for` loop.
4. However, the remaining iterations of the fixed-length inner `for` loop continue executing.
5. Since no more worker outputs are expected, each remaining `get(timeout=_TIMEOUT)` call times out.

In this minimal example, the total elapsed time with `preemptive_threshold=1.0` is approximately:

```text
num_workers * _TIMEOUT
```

This appears to consist of:

```text
1 initial timeout
+ (num_workers - 1) timeouts after all worker outputs have been received
```

Would it be appropriate to stop the inner loop once all worker outputs have been received?

For example:

```python
for _ in range(self.num_workers):
    if len(recv) >= self.num_workers:
        break
    ...
```

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a1a107003252a3ab2a0830702d21b7f46caff6d7`.  There
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
{"case_id": "pytorch_rl__3840__a1a1070",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
