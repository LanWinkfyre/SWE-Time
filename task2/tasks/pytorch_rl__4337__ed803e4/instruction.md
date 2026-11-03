# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] SACLossConfig cannot be instantiated: fields of the other SAC variant are forwarded to the loss

## Describe the bug

`_make_sac_loss` passes every `SACLossConfig` field to the loss constructor, but `SACLoss` and `DiscreteSACLoss` accept different kwargs. Since #3693 added `action_space`, `num_actions` and `target_entropy_weight` to the config, instantiating it fails for both variants:

* `discrete=False` (the default): `SACLoss` receives `action_space`, `num_actions` and `target_entropy_weight`
* `discrete=True`: `DiscreteSACLoss` receives `value_network`, `action_spec`, `delay_actor` and `delay_value`

This also breaks `sota-implementations/sac_trainer`, whose config uses `loss@loss: sac`. Calling `instantiate(cfg.loss)` on the composed config raises the same error.

## To Reproduce

```python
from hydra.utils import instantiate
from torchrl.trainers.algorithms.configs.modules import (
    MLPConfig,
    TanhNormalModelConfig,
    TensorDictModuleConfig,
)
from torchrl.trainers.algorithms.configs.objectives import SACLossConfig

cfg = SACLossConfig(
    actor_network=TanhNormalModelConfig(
        network=MLPConfig(in_features=10, out_features=4, depth=2, num_cells=32),
        in_keys=["observation"],
        out_keys=["action"],
    ),
    qvalue_network=TensorDictModuleConfig(
        module=MLPConfig(in_features=12, out_features=1, depth=2, num_cells=32),
        in_keys=["observation", "action"],
        out_keys=["state_action_value"],
    ),
)
instantiate(cfg)
```

```bash
hydra.errors.InstantiationException: Error in call to target 'torchrl.trainers.algorithms.configs.objectives._make_sac_loss':
TypeError("SACLoss.__init__() got an unexpected keyword argument 'action_space'. Did you mean 'action_spec'?")
```

With `discrete=True` added to the same config:

```bash
hydra.errors.InstantiationException: Error in call to target 'torchrl.trainers.algorithms.configs.objectives._make_sac_loss':
TypeError("DiscreteSACLoss.__init__() got an unexpected keyword argument 'value_network'. Did you mean 'qvalue_network'?")
```

## Expected behavior

The config builds a `SACLoss` or a `DiscreteSACLoss`, and each constructor only receives the fields it accepts.

## System info

* TorchRL source checkout at `ed803e488dbfd0632453e2fbc304831d233540d8`
* Linux, Python 3.13
* PyTorch `2.11.0`, TensorDict `0.14.2`, hydra-core `1.3.6`

## Reason and Possible fixes

`_make_iql_loss` already handles the same situation: it pops `action_space` before building `IQLLoss` and `deactivate_vmap` before building `DiscreteIQLLoss`. `_make_sac_loss` needs the same per-variant filtering. I checked the other loss factories against their targets' `__init__` signatures and none of them have this problem. No test instantiates `SACLossConfig`, which is probably why it went unnoticed. I have a fix with a regression test and will open a PR.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ed803e488dbfd0632453e2fbc304831d233540d8`.  There
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
{"case_id": "pytorch_rl__4337__ed803e4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
