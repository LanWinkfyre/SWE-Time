# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Maybe a bug, stepCounter docs blurry about a behavior in MARL

## Describe the bug
On the 0.11 torchRL doc:
truncated_key (str, optional) – the key where the truncated entries should be written. Defaults to "truncated", which is recognised by data collectors as a reset signal. This argument can only be a string (not a nested key) as it will be matched to each of the leaf done key in the parent environment (eg, a ("agent", "done") key will be accompanied by a ("agent", "truncated") if the "truncated" key name is used).

I'm not sure If I understood incorrectly, but from the exemple below the "agent" key (here "archers") aren't updated with their ("archers", "done") if update_done = True nor ("archers", "truncated") keys.

## To Reproduce

Steps to reproduce the behavior.

Please try to provide a minimal example to reproduce the bug. Error messages and stack traces are also helpful.

Please use the markdown code blocks for both code and stack traces.

```
from torchrl.modules import ProbabilisticActor, MLP
from torchrl.collectors import SyncDataCollector
from torchrl.envs import PettingZooWrapper, TransformedEnv, Compose, DTypeCastTransform, StepCounter
from pettingzoo.butterfly import knights_archers_zombies_v10
from tensordict.nn import TensorDictModule
import torch
import math

def _create_env(**kwargs):

    env = knights_archers_zombies_v10.parallel_env(**{
        key: kwargs[key] for key in [
            "render_mode", "num_archers", "num_knights", "max_zombies",
            "spawn_rate", "max_arrows", "vector_state", "use_typemasks"
        ]
    })

    group_map = {}
    if kwargs.get("num_knights", 0) > 0:
        group_map["knights"] = []
    if kwargs.get("num_archers", 0) > 0:
        group_map["archers"] = []
    
    for agent in env.possible_agents:
        type, id = agent.split("_")
        if type == "archer":
            group_map["archers"].append(agent)
        elif type == "knight":
            group_map["knights"].append(agent)
        else:
            ValueError("Wrong agent type")

    env = PettingZooWrapper(
        env,
        return_state=kwargs.get("return_state"),
        group_map=group_map,
        use_mask=kwargs.get("use_mask"),
        categorical_actions=kwargs.get("categorical_actions"),
        done_on_any=kwargs.get("done_on_any"),
    )
    env = TransformedEnv(env, Compose(
                                    DTypeCastTransform(torch.float64, torch.float32),
                                    StepCounter(128)))
    return env

class ActorModel(torch.nn.Module):
    def __init__(self, input_shape, output_dim, hidden_dim=256, depth=3):
        super().__init__()
        self.flatten = torch.nn.Flatten(-2)
        self.mlp = MLP(
            in_features=input_shape,
            out_features=output_dim,
            num_cells=hidden_dim,
            depth=depth
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.mlp(x)

if __name__ == "__main__":

    ENV_SPAWN_RATE = 10
    ENV_NUM_ARCHERS = 4
    ENV_NUM_KNIGHTS = 0
    ENV_MAX_ZOMBIES = 10
    ENV_MAX_ARROWS = 9

    AC_HIDDEN_DIM = 256
    AC_DEPTH = 2

    C_FRAMES_PER_BATCH = 2048
    
    default_env_args = {
        "render_mode": None,
        "vector_state": True, 
        "use_typemasks": True, 
        "return_state": True, 
        "use_mask": True, 
        "categorical_actions": True, 
        "done_on_any": False,
    }

    env = _create_env(num_archers = ENV_NUM_ARCHERS, num_knights = ENV_NUM_KNIGHTS, max_zombies = ENV_MAX_ZOMBIES, spawn_rate = ENV_SPAWN_RATE, max_arrows = ENV_MAX_ARROWS, **default_env_args)

    group = "archers"

    actor = ProbabilisticActor(
        TensorDictModule(ActorModel(
            input_shape=math.prod(env.observation_spec[group]["observation"].shape[-2:]),
            output_dim=env.action_spec[group]["action"].space.n,
            hidden_dim=AC_HIDDEN_DIM,
            depth=AC_DEPTH
            ), 
        in_keys=[(group, "observation")],
        out_keys=[(group, "logits")]
        ),
        in_keys=[(group, "logits")],
        out_keys=[(group, "action")],
        distribution_class=torch.distributions.Categorical
    )

    collector = SyncDataCollector(
        create_env_fn = env,
        policy = actor,
        frames_per_batch = C_FRAMES_PER_BATCH,
        total_frames = -1,
    )

    batch = next(iter(collector))
    print(batch["step_count"][batch["next", "truncated"]])
    print(batch["step_count"][batch["next", "archers", "truncated"][:, 0]])
```

```
tensor([127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
        127, 127])
tensor([], dtype=torch.int64)
```

## Expected behavior

"next" "truncated" if updated by StepCounter should update all agents truncated keys also ?
"next" "done" if update_done =True shoud also update "next" "agent "done" keys ?

Describe the characteristic of your environment:
torchRL 0.11 

## Reason and Possible fixes

Maybe I don't understand the doc correctly, but in the truncated_keys/done_keys list made in stepCounter, it only check for _reset signal and when done_on_any if False, agent arn't updated ?

## Checklist

- [ ] I have checked that there is no similar issue in the repo (**required**)
- [ ] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [ ] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3fe392b63c849e22b9ce10860c0ae2c4de9b6fd1`.  There
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
{"case_id": "pytorch_rl__3400__3fe392b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
