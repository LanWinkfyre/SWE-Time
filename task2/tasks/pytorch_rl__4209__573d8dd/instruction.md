# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] V-trace advantage bootstraps from the next trajectory at truncated steps

## Describe the bug

`vtrace_advantage_estimate` computes the IMPALA advantage `rho_s * (r_s + gamma * v_{s+1} - V(x_s))` with `v_{s+1}` taken as the v-trace target shifted one step along time:

```python
vs_t_plus_1 = torch.cat([vs[..., 1:, :], next_state_value[..., -1:, :]], dim=time_dim)
```

`next_state_value` is only used for the final step of the batch. When a batch holds several trajectories concatenated along time (the normal collector layout), the shifted entry at an intermediate `done` step is the v-trace target of the *first step of the next trajectory*. For a truncated step (`done & ~terminated`) the discount is `gamma`, so the next episode's value estimate leaks into the advantage.

The `vs` recursion already cuts at `done` (`done_discounts = gamma * not_done`), so `value_target` is correct; only the advantage at in-batch truncations is wrong. Terminal steps are unaffected because their discount is already zero.

`VTrace` passes `("next", "done")` and `("next", "terminated")` separately, so any IMPALA / PPO-with-VTrace run whose rollouts contain time-limit truncations (gym `TimeLimit`, `StepCounter`, `max_frames_per_traj`) trains on advantages contaminated by the following episode's value at each truncation.

## To Reproduce

Two trajectories A=[t0, t1] truncated at t1 and B=[t2, t3], with V_A = 1, V_B = 100, r = 0, gamma = 1, on-policy (rho = c = 1). Every advantage must be 0.

```python
import torch
from torchrl.objectives.value.functional import vtrace_advantage_estimate

T = 4
done = torch.tensor([[False], [True], [False], [False]])
terminated = torch.zeros_like(done)
reward = torch.zeros(T, 1)
state_value = torch.tensor([[1.0], [1.0], [100.0], [100.0]])
next_state_value = state_value.clone()
log_pi = log_mu = torch.zeros(T, 1)

adv, vs = vtrace_advantage_estimate(
    1.0, log_pi, log_mu, state_value, next_state_value, reward,
    done=done, terminated=terminated,
)
print("advantage:", adv.squeeze(-1).tolist())
print("vs       :", vs.squeeze(-1).tolist())
```

Output on `main` (573d8dd):

```
advantage: [0.0, 99.0, 0.0, 0.0]
vs       : [1.0, 1.0, 100.0, 100.0]
```

`99.0 = 0 + 100 - 1`: the truncated step at t=1 bootstrapped from trajectory B's v-trace target instead of its own next value.

## Expected behavior

`advantage: [0.0, 0.0, 0.0, 0.0]`. At a truncated step the only valid `v_{s+1}` is `V(x_{s+1}) = next_state_value[s]`, which is what the function already does for the batch's last step and what `generalized_advantage_estimate` does at every truncation.

## System info

- torchrl `main` at 573d8dd, tensordict 0.14.0, torch 2.14.0+cpu, Python 3.11, Windows 11 (CPU only)

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `573d8ddea6961fbce3e4f1404d6adef19d8c3ba4`.  There
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
{"case_id": "pytorch_rl__4209__573d8dd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
