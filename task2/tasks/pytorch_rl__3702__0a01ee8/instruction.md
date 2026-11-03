# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] PettingZoo: action mask with ParallelEnv and `done_on_any=False` causes `KeyError`

## Describe the bug

The PettingZoo adapter at `torchrl.envs.libs.pettingzoo` supports action masks for both AEC and Parallel env types. `_update_action_mask` is used to update the actual mask after every env step. A problem arises when an agent is removed from the pool of active agents and `done_on_any` is `False`. 

A snippet of the function can be seen here:

```python
    def _update_action_mask(self, td, observation_dict, info_dict):
        # Since we remove the action_mask keys we need to copy the data
        observation_dict = copy.deepcopy(observation_dict)
        info_dict = copy.deepcopy(info_dict)
        # In AEC only one agent acts, in parallel env self.agents contains the agents alive
        agents_acting = self.agents if self.parallel else [self.agent_selection]

        for group, agents in self.group_map.items():
            if self.has_action_mask[group]:
                group_mask = td.get((group, "action_mask"))
                group_mask += True
                for index, agent in enumerate(agents):
                    agent_obs = observation_dict[agent]
                    agent_info = info_dict[agent]
                    if isinstance(agent_obs, dict) and "action_mask" in agent_obs:
                        if agent in agents_acting:
                            group_mask[index] = torch.tensor(
                                agent_obs["action_mask"],
                                device=self.device,
                                dtype=torch.bool,
                            )
```

First, `self.group_map` is created at initialization, so this loops over all agents regardless of status. Also, `self.has_action_mask[group]` is similarly static, being constructed at initialization.  

The problem arises when agents are removed from the pool of active agents in a ParallelEnv; the outer loop iterates over all agents, the inner loop does the same (assuming all agents have masks), but then a `KeyError` is hit when evaluating `agent_obs = observation_dict[agent]` because PettingZoo expects that you remove inactive agents from the observation. 

I think the guard rail was intended to be using `if agent in agents_acting`, but that's used _after_ the observation and info dicts are accessed, so it doesn't avoid the `KeyError`.

## To Reproduce

I have a custom environment, but reproduction could be done in any environment with a `ParallelEnv` with action masks and `done_on_any=False`. 

None of the stock `PettingZoo` envs have this combination of options (`ParallelEnv` with action masking and `done_on_any`), so it's difficult to provide a reproduction pathway, but the problem should be apparent from the code path.

## Expected behavior

A check is performed to ensure that agents are present in the environment before trying to update their action mask.

## Screenshots

N/A

## System info

torchrl 0.11.0 (but still present in latest/dev)

## Additional context

N/A

## Reason and Possible fixes

I will prepare a PR with a simple fix. 

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [ ] I have provided a minimal working example to reproduce the bug (**required**)
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
{"case_id": "pytorch_rl__3702__0a01ee8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
