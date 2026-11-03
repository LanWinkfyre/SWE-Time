# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] KeyError: 'action_key requested but more than one key present in the environment' when `space.Dict` `action_space`

## Describe the bug

I have a `gymnasium` environment of the form:

```
import gymnasium as gym
from gymnasium import spaces

class MyEnvironment(gym.Env):
    def __init__(self, ...):
   
        ...

        self.action_space = spaces.Dict(a=spaces.Discrete(2), b=spaces.Box(0, 1, shape=[1]))
        self.observation_space = spaces.Box(0, 1, shape=[1])

        ...
```

I'm registering the environment then running:

```
import gymnasium as gym
from torchrl.envs import GymWrapper

env = GymWrapper(gym.make("MyEnvironment", ...))
env.rollout(40)
```

But then seeing this error:

```
KeyError: 'action_key requested but more than one key present in the environment'
```

And, when I attempt to use a tuple instead:

```
self.action_space = spaces.Tuple([spaces.Box(-1, 1, shape=[1]),
                                                           spaces.Box(0, 1, shape=[1])])
```

I see another error:

```
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/common.py", line 2636, in rollout
    tensordicts = self._rollout_stop_early(
                  ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/common.py", line 2730, in _rollout_stop_early
    tensordict = self.step(tensordict)
                 ^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/common.py", line 1506, in step
    next_tensordict = self._step(tensordict)
                      ^^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/gym_like.py", line 298, in _step
    action = self.read_action(action)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/libs/gym.py", line 917, in read_action
    action = super().read_action(action)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/envs/gym_like.py", line 188, in read_action
    return self.action_spec.to_numpy(action, safe=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/project/venv/lib/python3.11/site-packages/torchrl/data/tensor_specs.py", line 1287, in to_numpy
    return val.detach().cpu().numpy()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Internal error: NestedTensorImpl doesn't support sizes. Please file an issue.
```

The rollout succeeds when the `spaces.Box` instances have the _exact_ same arguments, but it wasn't clear from the documentation that this was required. Only that they needed to have the same dimension and `dtype`.

## Expected behavior

The documentation says to be cautious when using `spaces` but also says torch RL supports `spaces.Dict` and `spaces.Tuple`. I would expect a rollout with either of these action spaces to succeed. Is there an idiomatic way to represent heterogeneous action spaces?

## System info

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```

0.6.0 1.26.4 3.11.2 (v3.11.2:878ead1ac1, Feb  7 2023, 10:02:41) [Clang 13.0.0 (clang-1300.0.29.30)] darwin
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `642588ea4cb93f0cd2817e7467c3ceb66f925139`.  There
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
{"case_id": "pytorch_rl__2716__642588e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
