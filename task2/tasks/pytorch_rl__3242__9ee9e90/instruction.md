# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] ActionMask fails for MultiDiscrete space with homogeneous nvec due to incorrect spec conversion

## Describe the bug

The conversion logic for `gymnasium.spaces.MultiDiscrete`, specifically for a spec with a homogeneous `nvec` (e.g., `[15, 15]`), incorrectly assumes it represents a batch of vectorized environments. This logic was introduced in #1519 to add compatibility for Gymnasium's vectorized environments.

As a result, an action space like `MultiDiscrete([15, 15])` is converted to a stacked `Categorical(shape=torch.Size([2]), n=15)` instead of the correct `MultiCategorical(nvec=[15, 15])`.

This incorrect spec causes the `ActionMask` transform to fail with a `RuntimeError` due to a shape mismatch, as it expects a mask compatible with a `(2, 15)` spec but receives a mask intended for a `(15, 15)` spec (e.g., a board game action mask). This appears to be an unintended side effect of the changes in #1519 that affects single-agent environments with multi-dimensional discrete action spaces.

## To Reproduce

The following minimal example uses a simple board game-like environment with a `MultiDiscrete([5, 5])` action space to reproduce the error.

```python
import gymnasium as gym
from gymnasium import spaces
from torchrl.envs import GymWrapper, TransformedEnv
from torchrl.envs.transforms import ActionMask
from torchrl.envs.utils import check_env_specs


# 1. Define a minimal environment with a homogeneous MultiDiscrete action space
class TestEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.MultiDiscrete([5, 5])
        # The action mask is a 5x5 grid
        self.observation_space = spaces.Dict(
            {
                "observation": spaces.Box(low=0, high=1, shape=(5, 5)),
                "action_mask": spaces.Box(low=0, high=1, shape=(5, 5), dtype=bool),
            }
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        return self.observation_space.sample(), 0.0, False, False, {}


# 2. Wrap the environment with GymWrapper and ActionMask
env_gym = TestEnv()
env = GymWrapper(env_gym, categorical_action_encoding=True)

# This is where the spec is incorrectly converted
# Expected: MultiCategorical(nvec=[5, 5]), shape=(5, 5)
# Actual: Categorical(n=5), shape=(2,)
print("Incorrectly converted action spec:", env.action_spec)
check_env_specs(env)

env_transformed = TransformedEnv(env, ActionMask())

print("Incorrectly converted action spec:", env_transformed.action_spec)
check_env_specs(env_transformed)
```

```bash
Incorrectly converted action spec: Categorical(
    shape=torch.Size([2]),
    space=CategoricalBox(n=5),
    device=cpu,
    dtype=torch.int64,
    domain=discrete)
2025-11-26 14:15:16,982 [torchrl][INFO]    check_env_specs succeeded! [END]
Incorrectly converted action spec: Categorical(
    shape=torch.Size([2]),
    space=CategoricalBox(n=5),
    device=cpu,
    dtype=torch.int64,
    domain=discrete)
Traceback (most recent call last):
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\data\tensor_specs.py", line 3920, in update_mask
    mask = mask.expand(_remove_neg_shapes(*self.shape, self.space.n))
RuntimeError: The expanded size of the tensor (2) must match the existing size (5) at non-singleton dimension 0.  Target sizes: [2, 5].  Tensor sizes: [5, 5]

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "d:\project\Gomoku-RL\test1.py", line 44, in <module>
    check_env_specs(env_transformed)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\utils.py", line 759, in check_env_specs
    real_tensordict = env.rollout(
        3,
    ...<3 lines>...
        break_when_any_done=break_when_any_done,
    )
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\common.py", line 3362, in rollout
    tensordict = self.reset(tensordict)
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\common.py", line 2859, in reset
    tensordict_reset = self._reset(tensordict, **kwargs)
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\transforms\transforms.py", line 1290, in _reset
    tensordict_reset = self.transform._reset(tensordict, tensordict_reset)
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\transforms\transforms.py", line 9020, in _reset
    return self._call(tensordict_reset)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\envs\transforms\transforms.py", line 9013, in _call
    self.action_spec.update_mask(mask.to(self.action_spec.device))
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\project\Gomoku-RL\.venv\Lib\site-packages\torchrl\data\tensor_specs.py", line 3922, in update_mask
    raise RuntimeError("Cannot expand mask to the desired shape.") from err
RuntimeError: Cannot expand mask to the desired shape.
```

## Expected behavior

The `gym.spaces.MultiDiscrete([5, 5])` should be converted to a `torchrl.data.MultiCategorical` spec. The `action_spec` of the `GymWrapper` should have a shape that reflects the multi-dimensional nature of the action space (e.g., `(5, 5)`), not a stacked 1D representation.

Consequently, `ActionMask` should be able to receive the `(5, 5)` boolean mask from the environment and apply it to the `MultiCategorical` spec without any shape-related errors.

## System info

All package was installed from pip
 * torchrl: 0.0.0+unknown
 * numpy: 2.3.5
 * gymnasium: 1.2.2
 * python: 3.13.8 (main, Oct  7 2025, 15:31:04) [MSC v.1944 64 bit (AMD64)]
 * platform: win32

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9ee9e90e55dc18ffb8a431f8badd4606ad55b1d5`.  There
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
{"case_id": "pytorch_rl__3242__9ee9e90",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
