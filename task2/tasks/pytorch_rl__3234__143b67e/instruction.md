# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] **TrajectoryBatcher** high-level util for complete episode batching

## Motivation

When using `MultiSyncDataCollector` with `split_trajs=True`, it is surprisingly difficult to obtain a batch of **N complete trajectories**.
Many RL algorithms (Monte Carlo / REINFORCE, episodic PPO rollouts, imitation learning, some RLHF setups) require full episodes padded into a single batch.

Right now users need to manually:

* track `traj_ids`,
* rebuild trajectories across collector iterations,
* detect completion via `mask` / `done`,
* pad variable-length episodes,
* optionally discard “mixed-policy” episodes when the policy is updated.

This logic is both error-prone and reimplemented repeatedly in user code.

There is currently no high-level utility in TorchRL that provides “give me exactly N full episodes as a padded TensorDict”, even though the underlying collectors already expose all the needed information.

## Solution

I propose a new utility, tentatively named **`TrajectoryBatcher`**, in `torchrl.collectors.utils`.

It would wrap any TorchRL collector and yield batches of exactly `num_trajectories` full episodes, reconstructed across collector steps and padded to `max_length`. Example:

```python
batcher = TrajectoryBatcher(
    collector,
    num_trajectories=32,
    strict_on_policy=True,
)

batch = next(iter(batcher))
batch["observation"].shape  # [32, max_len, obs_dim]
batch["action"].shape       # padded
batch["mask"].shape         # valid-step mask
```

Features:

* reconstruct trajectories split across collector iterations (using `traj_ids`)
* optional **strict on-policy** mode (“burn” ongoing trajectories after a policy update)
* padded output using standard TensorDict conventions
* compatible with multi-worker collectors without resetting environments

I already have a working prototype and can contribute the implementation, documentation, and unit tests.

## Alternatives

* Users manually stitch trajectories in Python (complex and repetitive).
* Resetting environments at every update is possible but costly and problematic with multi-process collectors.
* Using `frames_per_batch` as a proxy for episodes is unreliable and does not guarantee complete trajectories.

These alternatives are not ideal and introduce unnecessary boilerplate for common RL workflows.

## Additional context

This feature would make it much easier to train Monte Carlo / episodic algorithms on top of TorchRL collectors, and aligns with patterns commonly found in other RL libraries (e.g., SB3 rollouts, RLlib sample batches, Acme episodes).

## Checklist

* [x] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `143b67ef3473a2df2429472f932dde3ea8f14fb0`.  There
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
{"case_id": "pytorch_rl__3234__143b67e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
