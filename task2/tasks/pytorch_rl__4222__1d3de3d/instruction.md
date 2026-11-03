# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Hydra Config _target_ values are unimportable (KLRewardTransform, StorageEnsembleWriter, Lion)

## Describe the bug

Three Hydra Config dataclasses ship `_target_` strings that cannot be imported, so `hydra.utils.instantiate` fails. `test/test_configs.py` already documents all three in `_CONFIG_PARITY_UNRESOLVED` and skips them, so CI stays green.

This issue only asks maintainers to decide: **fix the paths + kwargs, redirect, or delete the Configs.** It is not a request for a large refactor.

## To Reproduce

### 1. `KLRewardTransformConfig`

```789:794:torchrl/trainers/algorithms/configs/transforms.py
class KLRewardTransformConfig(TransformConfig):
    """Configuration for KLRewardTransform."""

    in_keys: list[str] | None = None
    out_keys: list[str] | None = None
    _target_: str = "torchrl.envs.transforms.llm.KLRewardTransform"
```

- `torchrl.envs.transforms.llm` does not exist. The class lives at `torchrl.envs.llm.transforms.kl.KLRewardTransform` (`torchrl/envs/llm/transforms/kl.py:159`).
- The Config only exposes `in_keys` / `out_keys`. The real constructor (`kl.py:213-228`) requires `ref_model` (or `ref_model_factory`) and accepts `coef`, `tokenizer`, `assistant_only`, `device`, `add_to_reward`, `log_prob_key`, `padding_side`, `use_ray_service`. Instantiating with the Config fields alone cannot build a working transform.
- The class itself is documented as legacy; `RetrieveKL` (`kl.py:957`) is the recommended replacement and has **no** Config.

### 2. `StorageEnsembleWriterConfig`

```291:296:torchrl/trainers/algorithms/configs/data.py
class StorageEnsembleWriterConfig(StorageConfig):
    """Configuration for storage ensemble writer."""

    _target_: str = "torchrl.data.replay_buffers.StorageEnsembleWriter"
    writers: list[Any] = MISSING
    transforms: list[Any] = MISSING
```

`StorageEnsembleWriter` does not exist. The writer ensemble class is `WriterEnsemble` (`torchrl/data/replay_buffers/writers/ensemble.py:44`), and there is already a working `WriterEnsembleConfig` (`data.py:79`) targeting `torchrl.data.replay_buffers.WriterEnsemble`.

### 3. `LionConfig`

```304:312:torchrl/trainers/algorithms/configs/utils.py
class LionConfig(ConfigBase):
    """Configuration for Lion optimizer."""

    lr: float = 1e-4
    betas: tuple[float, float] = (0.9, 0.99)
    weight_decay: float = 0.0
    _target_: str = "torch.optim.Lion"
    _partial_: bool = True
```

`torch.optim.Lion` is not available in the torch versions TorchRL currently supports.

### Already recorded in the parity test

```135:150:test/test_configs.py
_CONFIG_PARITY_UNRESOLVED = {
    ...
    "StorageEnsembleWriterConfig": "_target_ references torchrl.data.replay_buffers."
    "StorageEnsembleWriter, which does not exist in the current codebase.",
    "KLRewardTransformConfig": "_target_ references torchrl.envs.transforms.llm, "
    "which does not exist; KLRewardTransform now lives in "
    "torchrl.envs.llm.transforms.kl.",
    "LionConfig": "_target_ references torch.optim.Lion, which is not available in "
    "the torch versions TorchRL currently supports.",
}
```

Those three names are skipped at `test/test_configs.py:237-242`.

## Expected behavior

Each public Config either:

- instantiates the class it names, with constructor kwargs that match that class, or
- is redirected to the supported replacement (`RetrieveKL`, `WriterEnsemble`, a supported optimizer), or
- is removed so Hydra users are not pointed at a dead `_target_`.

Please pick one of those three options per Config. Do not treat this issue as a request to redesign the Hydra layer.

## Screenshots

N/A

## System info

Observed on a source checkout of pytorch/rl at `1d3de3db`.

## Additional context

`KLRewardTransformConfig` is registered as `transform/kl_reward` and `LionConfig` as `optimizer/lion` in `torchrl/trainers/algorithms/configs/__init__.py` (around lines 621 and 744). Anyone composing those nodes through Hydra hits an import error at instantiate time.

## Reason and Possible fixes

The skip reasons in `_CONFIG_PARITY_UNRESOLVED` already state the import failures. Suggested resolutions, for maintainers to choose:

- `KLRewardTransformConfig`: retarget to `torchrl.envs.llm.transforms.kl.KLRewardTransform` and add the real kwargs, add a `RetrieveKLConfig`, or delete the Config.
- `StorageEnsembleWriterConfig`: delete it (duplicate of `WriterEnsembleConfig`) or retarget / rehome it if a storage-level ensemble writer is still intended.
- `LionConfig`: retarget to a third-party Lion that TorchRL actually depends on, or delete it.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1d3de3dbd416877c02b2f44fe66a615fe55fb8e9`.  There
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
{"case_id": "pytorch_rl__4222__1d3de3d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
