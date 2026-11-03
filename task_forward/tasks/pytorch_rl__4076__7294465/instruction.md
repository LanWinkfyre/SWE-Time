# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] SoftUpdate fails for list-valued SAC critics

## History

Follow-up to #2589 and #3500. That fix made list-valued SAC critics work during loss evaluation, but its regression test did not construct a target updater. Found while implementing TQC for #1623.

## Bug

`SoftUpdate(SACLoss(...))` fails in `TargetNetUpdater.init_` when `qvalue_network` is a list. `_sources.select(...)` runs on locked list-backed parameter storage, so delayed critic updates cannot start.

<details>
<summary>Reproduction</summary>

```python
import torch
from torch import nn
from tensordict.nn import NormalParamExtractor, TensorDictModule

from torchrl.data import Bounded
from torchrl.modules import ProbabilisticActor, ValueOperator
from torchrl.modules.distributions import TanhNormal
from torchrl.objectives import SACLoss, SoftUpdate

obs_dim, action_dim = 3, 4
spec = Bounded(-torch.ones(action_dim), torch.ones(action_dim), (action_dim,))
actor = ProbabilisticActor(
    TensorDictModule(
        nn.Sequential(nn.Linear(obs_dim, 2 * action_dim), NormalParamExtractor()),
        in_keys=["observation"],
        out_keys=["loc", "scale"],
    ),
    in_keys=["loc", "scale"],
    spec=spec,
    distribution_class=TanhNormal,
)

class Critic(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(obs_dim + action_dim, 1)

    def forward(self, observation, action):
        return self.linear(torch.cat((observation, action), -1))

critics = [
    ValueOperator(Critic(), in_keys=["observation", "action"]),
    ValueOperator(Critic(), in_keys=["observation", "action"]),
]
loss = SACLoss(actor, critics, num_qvalue_nets=2)
SoftUpdate(loss, eps=0.5)
```

Actual: construction fails with `RuntimeError: Cannot modify locked TensorDict` at `_sources.select(...)`.

Expected: construction succeeds and both delayed critics can be updated.

</details>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7294465173cb23121386db0ce115abba54fc4a28`.  There
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
{"case_id": "pytorch_rl__4076__7294465",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
