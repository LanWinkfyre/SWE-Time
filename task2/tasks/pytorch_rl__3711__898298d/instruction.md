# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] LSTMModule Bug

## Describe the bug

In LSTMModule, during the forward pass, the hidden states can be incorrectly removed. We believe this is because `inv_pad_sequence` expects it to be stored at the end of the trajectory step and removes the following steps accordingly, while in reality, the hidden state is stored at the max number of steps of the batch. This means trajectories with fewer steps than the max will see their hidden state incorrectly be zero. 

## To Reproduce

Steps to reproduce the behavior.

Please try to provide a minimal example to reproduce the bug. Error messages and stack traces are also helpful.

Please use the markdown code blocks for both code and stack traces.

```python
import torch
from tensordict import TensorDict
from torchrl.modules import LSTMModule
from torchrl.modules.tensordict_module.rnn import set_recurrent_mode

B = 1  # Batch Size (1 Env)
T = 5  # Time Steps
F = 2  # Observation Features
H = 4  # Hidden Size

is_init1 = torch.zeros(B, T, 1, dtype=torch.bool)
is_init1[0, 3] = True 

obs1 = torch.ones(B, T, F)
obs1[0, 3:] = 2.0

data = TensorDict({
    "obs": obs1,
    "is_init": is_init1
}, [B, T])

lstm = LSTMModule(
    input_size=F, 
    hidden_size=H, 
    in_key="obs", 
    out_keys=["action_features", ("next", "recurrent_state_h"), ("next", "recurrent_state_c")]
)

with set_recurrent_mode(True), torch.no_grad():
    data_recurrent = lstm(data)
print(data_recurrent["next", "recurrent_state_h"])
```

## Expected behavior

I'd expect `data_recurrent["next", "recurrent_state_h"]` to be populated at the steps of the end of each trajectory, but instead we see zeros at the end of trajectory 2.

## Screenshots

If applicable, add screenshots to help explain your problem.

## System info

Describe the characteristic of your environment:
 * Describe how the library was installed (pip, source, ...)
 * Python version
 * Versions of any other relevant libraries

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```

## Additional context

Add any other context about the problem here.

## Reason and Possible fixes

We can contribute a PR to fix this, but it's because the hidden states are stored at the max length trajectory location, and then when we remove the padding, we remove the end of the padding for shorter trajectories, removing the stored hidden states. 

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `898298dfcd112c337d44523dd1f28bb6b663c1e4`.  There
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
{"case_id": "pytorch_rl__3711__898298d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
