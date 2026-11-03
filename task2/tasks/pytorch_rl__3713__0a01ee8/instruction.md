# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Implementing HER(Hindsight Experience Replay)

Motivation
Goal-conditioned RL is sparse-reward by nature. An agent manipulating objects, navigating to targets, or following language instructions almost always fails early in training — the desired goal is never reached, so the reward signal is nearly always zero and gradient flow stalls.

HER (Andrychowicz et al., 2017, https://arxiv.org/abs/1707.01495) solves this by relabeling failed trajectories at sample time: the achieved state is substituted as the goal, the reward is recomputed under that relabeled goal, and the transition becomes a valid positive training example. This turns failures into learning signal with no architectural changes to the policy or loss.

This is the standard baseline for any robotics or manipulation task. OpenAI Gym's GoalEnv was designed around it. Every major RL library (Stable-Baselines3, CleanRL, RLlib) has an implementation. TorchRL does not.

HER belongs in the replay buffer layer, not the loss or env. Relabeling happens at sample time, which is consistent with how PrioritizedSampler and SliceSampler extend sampling behavior without touching storage.


from torchrl.data import ReplayBuffer, LazyMemmapStorage
from torchrl.data.replay_buffers.samplers import HERSampler, HindsightStrategy

sampler = HERSampler(
    strategy=HindsightStrategy.FUTURE,  # "future" | "episode" | "random" | "final"
    her_ratio=0.8,           # fraction of sampled transitions to relabel
    goal_key="desired_goal",
    achieved_goal_key="achieved_goal",
    reward_fn=recompute_reward,  # Callable[[achieved, desired, info], Tensor]
)

rb = ReplayBuffer(storage=LazyMemmapStorage(100_000), sampler=sampler)
The buffer stores transitions with the original goal. HERSampler intercepts the sample call, selects relabeling candidates according to strategy, substitutes achieved_goal into desired_goal, calls reward_fn to recompute the scalar reward, and returns the modified tensordict. The policy and loss see nothing unusual.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0a01ee81fa420c76fb4259b2dfa09264338a9609`.  There
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
{"case_id": "pytorch_rl__3713__0a01ee8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
