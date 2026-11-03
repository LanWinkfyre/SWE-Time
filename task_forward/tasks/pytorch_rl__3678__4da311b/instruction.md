# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[RFC]Making sequence-based RL first-class in TorchRL

##Motivation 
TorchRL has all the building blocks for sequence-based RL — SliceSampler, split_trajectories, LSTMModule, TensorDictPrimer, traj_ids — but they are not designed to compose automatically. Users who want to train RNN or sequence-based policies (ACT, Decision Transformer, recurrent PPO) must manually wire them together and get the masking, trajectory key alignment, and hidden state resets right themselves. This RFC proposes making that pipeline explicit, safe, and ergonomic by default.

##Solution

1. Standardize trajectory key defaults
Align SliceSampler's default traj_key to auto-detect ("collector", "traj_ids") when present, falling back to "episode" for backward compatibility. This fixes a silent composability bug with no API break.

2. Add episode_start metadata from collectors
Emit ("collector", "episode_start") — a boolean flag marking the first step of each episode. Downstream code should not have to re-derive episode boundaries from done repeatedly.

3. Sequence sampling with built-in mask and lengths
Extend SliceSampler to return [B, T] TensorDicts with:


("collector", "mask")     # bool [B, T] — False on padded timesteps
("collector", "lengths")  # int  [B]
when strict_length=False. Users should not need to call split_trajectories() manually.

4. Safe hidden state reset for recurrent policies
Recurrent policies currently leak hidden state across episode boundaries unless the user manually configures TensorDictPrimer + is_init. The target behavior: if episode_start or is_init is present, hidden state resets automatically at those positions.

5. Mask-aware losses
Common loss modules should respect ("collector", "mask") if present, so padded timesteps do not contribute to the gradient. Start narrow — behavior cloning / imitation losses first.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4da311b961920bdbe3df4b3405e603416acd7e75`.  There
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
{"case_id": "pytorch_rl__3678__4da311b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
