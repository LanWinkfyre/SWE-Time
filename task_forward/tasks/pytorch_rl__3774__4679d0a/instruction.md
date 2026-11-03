# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[RFC] torchrl.modules.WorldModel — A General TensorDict-Native World Model Abstraction

## Overview

This RFC proposes adding `torchrl.modules.WorldModel`, a composable, TensorDict-native abstraction for learned environment dynamics, to serve as a general foundation for model-based RL workflows in TorchRL.

---

## Motivation

TorchRL has strong abstractions for environments (`EnvBase`), policies (`TensorDictModule`), data collection (`Collector`), replay buffers, and loss modules. Model-based RL, however, still requires users to write substantial glue code.

### What exists today

TorchRL ships Dreamer-specific components:

- `RSSMPrior`, `RSSMPosterior`, `RSSMRollout` — RSSM-specific dynamics (also V3 discrete variants)
- `ObsEncoder`, `ObsDecoder` — Conv stacks for pixel observations
- `DreamerActor` — distribution head for the imagination policy
- `WorldModelWrapper` — thin `TensorDictSequential(transition_model, reward_model)` with no rollout interface
- `ModelBasedEnvBase` / `DreamerEnv` — environment wrapper that calls `world_model(td)` in `_step()`
- `DreamerModelLoss`, `DreamerActorLoss`, `DreamerValueLoss` — losses coupled tightly to the RSSM + DreamerEnv stack

### The gap

There is no general abstraction for learned dynamics. Users implementing any world-model-based algorithm (MBPO, TD-MPC, DreamerV3, PlaNet, Iris, CWVAE, or a custom learned env) must:

1. Manually wrap each component with `TensorDictModule` and wire `in_keys`/`out_keys` by hand
2. Write a custom multi-step rollout loop (no standard `rollout(policy, horizon)` interface)
3. Accept that the losses (`DreamerActorLoss`) are tightly coupled to `DreamerEnv`, not to a generic dynamics interface
4. Write ~150 lines of boilerplate (`make_dreamer()` in `sota-implementations/dreamer/dreamer_utils.py`) before the training loop starts

The result: world-model workflows are effectively siloed from the rest of TorchRL. Imagined rollouts cannot be dropped into standard collectors, sequence replay buffers, or existing loss modules without significant adaptation.

## Proposed API

### `WorldModel`

```python
from torchrl.modules import WorldModel

world_model = WorldModel(
    encoder=encoder,               # TensorDictModule: obs → latent
    dynamics=dynamics,             # TensorDictModule: (latent, action) → next_latent
    reward_head=reward_head,       # TensorDictModule: next_latent → reward
    done_head=done_head,           # TensorDictModule: next_latent → done (optional)
    decoder=decoder,               # TensorDictModule: latent → obs_recon (optional)
    observation_key="observation",
    action_key="action",
    latent_key=("latent", "state"),
    next_latent_key=("next", "latent", "state"),
)
```

**Key methods:**

```python
# Encode a real observation into the latent space
latent_td = world_model.encode(tensordict)

# Take one imagined step given current latent and action
next_td = world_model.step(tensordict)

# Decode a latent back to observation space (requires decoder)
recon_td = world_model.decode(tensordict)

# Run an imagined rollout for `horizon` steps with a given policy
# Returns TensorDict of shape [batch, horizon] — same layout as a real rollout
imagined_td = world_model.rollout(
    start_td=start_td,
    policy=actor,
    horizon=15,
)
```

### `WorldModelLoss`

```python
from torchrl.objectives import WorldModelLoss

loss_module = WorldModelLoss(
    world_model,
    losses=["latent", "reward", "done", "reconstruction"],
    kl_weight=1.0,
    reconstruction_weight=1.0,
)

real_batch = replay_buffer.sample(batch_size=256)
loss_td = loss_module(real_batch)
# loss_td contains: loss_latent, loss_reward, loss_done, loss_reconstruction
```

### End-to-end training sketch

```python
# World model update (on real data)
real_batch = replay_buffer.sample(batch_size=256)
loss_td = model_loss(real_batch)
(loss_td["loss_latent"] + loss_td["loss_reward"]).backward()
model_opt.step()

# Actor/critic update (on imagined rollouts)
start_td = real_batch[:, 0]
imagined_td = world_model.rollout(start_td, policy=actor, horizon=15)
actor_loss_td = actor_loss(imagined_td)
actor_loss_td["loss_objective"].backward()
actor_opt.step()
```

## Compatibility with Existing TorchRL Infrastructure

| Component | Compatibility |
|---|---|
| `TensorDictReplayBuffer` | Imagined rollouts stored directly (same TensorDict layout) |
| `SliceSampler` | Imagined trajectories are sequences — sample subsequences for recurrent training |
| `GAE` / `MultiAgentGAE` | Value targets computed from imagined rollouts |
| `ClipPPOLoss`, `SACLoss` | Consume imagined TensorDicts without modification |
| `EnvBase` specs | `WorldModel` optionally validates against `observation_spec`, `action_spec` |
| `Collector` / `SyncDataCollector` | Imagined rollout interface mirrors real rollout interface |
| `DreamerEnv` (existing) | Remains supported; `WorldModel.rollout` is an alternative that avoids the `EnvBase` overhead |

---

## Migration Path for Dreamer Users

Existing `DreamerModelLoss`, `DreamerActorLoss`, `DreamerValueLoss` are **unchanged**. Users may optionally migrate:

```python
# Before (current Dreamer setup — ~150 LOC in make_dreamer())
world_model = WorldModelWrapper(
    TensorDictSequential(rssm_prior, rssm_posterior, ...),
    reward_model,
)
dreamer_env = DreamerEnv(world_model, ...)
imagined_td = dreamer_env.rollout(15, actor)

# After (with WorldModel abstraction)
world_model = WorldModel(
    encoder=obs_encoder,
    dynamics=TensorDictSequential(rssm_prior, rssm_posterior),
    reward_head=reward_mlp,
    done_head=None,
)
imagined_td = world_model.rollout(start_td, actor, horizon=15)
```

## Scope of Implementation

**New files:**
- `torchrl/modules/world_model.py` — `WorldModel`
- `torchrl/objectives/world_model_loss.py` — `WorldModelLoss`
- `test/test_world_model.py` — unit tests
- `tutorials/sphinx-tutorials/world_model.py` — tutorial

**Modified files:**
- `torchrl/modules/__init__.py` — export `WorldModel`
- `torchrl/objectives/__init__.py` — export `WorldModelLoss`
- `docs/source/reference/modules_models.rst` — add entry
- `docs/source/reference/objectives_other.rst` — add entry

---
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4679d0a4c0aec9c4542356918df83bf9eee2011b`.  There
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
{"case_id": "pytorch_rl__3774__4679d0a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
