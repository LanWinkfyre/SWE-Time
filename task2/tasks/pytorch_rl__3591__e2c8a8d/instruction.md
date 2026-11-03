# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Async TrajectoryBatcher + Replay Buffer integration with SliceSampler

Motivation
Off-policy and replay-based RL algorithms — particularly those using recurrent policies (RNNs/LSTMs), Hindsight Experience Replay (HER), or episodic PPO variants — require storing and sampling full episodes rather than random transitions. Currently, even with the TrajectoryBatcher utility added in #[original PR], there is no straightforward path to:

Collect episodes asynchronously in the background via collector.start()
Store complete, padded trajectory batches into a ReplayBuffer
Sample contiguous trajectory slices using SliceSampler
Users who want this workflow must manually wire together the async collector API, the replay buffer extend() call, and the trajectory-aware sampling tooling — which is error-prone and reimplemented repeatedly.

Solution
Extend TrajectoryBatcher (and/or add a companion utility/example) to support:

Async collection via collector.start(), so trajectory assembly happens while training continues
ReplayBuffer.extend() compatibility with the zero-padded [N, max_len, ...] TensorDicts produced by TrajectoryBatcher, including correct handling of the ("collector", "mask") field
SliceSampler integration, using ("collector", "traj_ids") as the trajectory key so sampled slices respect episode boundaries
A reference example demonstrating the full async collect → store → sample → train loop would also be included.

Alternatives
Manual wiring: Users can already combine collector.start(), TrajectoryBatcher, and ReplayBuffer themselves, but this requires deep familiarity with each API and is not documented anywhere.
Transition-level replay: Standard ReplayBuffer + RandomSampler works for transition-based algorithms but loses episode structure, which breaks recurrent policies and trajectory-dependent methods.
Keeping it synchronous: The original PR covers the synchronous on-policy case. This is sufficient for REINFORCE/episodic PPO but not for off-policy or sample-efficient workflows.
Additional context
Follows up #3584 which introduced TrajectoryBatcher for synchronous, on-policy episode batching. This PR targets the complementary off-policy / async use case.

Relevant existing APIs this builds on:

collector.start() / async collector interface
ReplayBuffer + LazyTensorStorage
SliceSampler (already traj-ID-aware)
Checklist
 I have checked that there is no similar issue in the repo
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e2c8a8d3a545e821e27e39a5166d7fae6d8e8ac4`.  There
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
{"case_id": "pytorch_rl__3591__e2c8a8d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
