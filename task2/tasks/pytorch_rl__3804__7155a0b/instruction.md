# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Evaluator.evaluate(weights=nn.Module) destroys nn.Module.state_dict()

# Description

Calling `Evaluator.evaluate(weights=<nn.Module>)` permanently empties the module's `state_dict()`. 

# Environment

Python    : 3.13.9
PyTorch   : 2.9.1+cu130
TorchRL   : 0.12.0
TensorDict: 0.12.4

# Minimal Reproduction

```python
import copy
import torch.nn as nn
from tensordict import TensorDict
from tensordict.nn import TensorDictModule
from torchrl.collectors import Evaluator
from torchrl.envs import GymEnv


# ── BUG ─────────────────────────────────────────────────────────────────────
policy_bug = TensorDictModule(nn.Linear(4, 2), ["observation"], ["action"])

print("=== BUG ===")
print(f"state_dict before: {len(policy_bug.state_dict())} keys")  # 2

evaluator = Evaluator(lambda: GymEnv("CartPole-v1"), policy_bug, max_steps=10)
evaluator.evaluate(TensorDict.from_module(policy_bug).data)       # triggers bug

print(f"state_dict after:  {len(policy_bug.state_dict())} keys")  # 0  ← BUG
assert len(policy_bug.state_dict()) == 0, "confirmed empty"

# ── WORKAROUND ───────────────────────────────────────────────────────────────
policy_fix = TensorDictModule(nn.Linear(4, 2), ["observation"], ["action"])

print("\n=== WORKAROUND ===")
print(f"state_dict before: {len(policy_fix.state_dict())} keys")  # 2

eval_copy = copy.deepcopy(policy_fix)          # deepcopy → Evaluator functionalizes only the copy
evaluator_fix = Evaluator(lambda: GymEnv("CartPole-v1"), eval_copy, max_steps=10)

weights = TensorDict.from_module(policy_fix).data.detach().clone().cpu()
evaluator_fix.evaluate(weights)                # pass TensorDictBase, not nn.Module

print(f"state_dict after:  {len(policy_fix.state_dict())} keys")  # 2  ← OK
assert len(policy_fix.state_dict()) == 2, "workaround works"
print("PASS")

```


# Below are analyses from LLM:

> Step 1 — Collector.__init__ "functionalizes" the policy
>   The first call to evaluate() lazily constructs a SyncDataCollector, whose
>   __init__ calls:
> 
>       TensorDict.from_module(policy, as_module=True)   # as_module=True !
> 
>   With as_module=True, TensorDictParams replaces the module's nn.Parameter
>   entries with a TensorDictParams wrapper stored in policy._param_td, and
>   clears policy._parameters.  The module still runs correctly because
>   __getattr__ falls back to _param_td, but state_dict() now returns {}.
> 
> Step 2 — to_module() with plain tensors never restores _parameters
>   On every subsequent evaluate() call, the evaluator syncs weights via:
> 
>       weights_td.to(device).to_module(self._policy)
> 
>   The internal _set_tensor_dict() helper does:
> 
>       out = _parameters.pop(name, None)   # removes the key
>       ...
>       if isinstance(tensor, nn.Parameter):
>           _parameters[name] = tensor      # only restored if tensor IS a Parameter
>       else:
>           __dict__[name] = tensor          # plain tensor → written to __dict__ only
> 
>   Because TensorDict.from_module(policy).data returns plain Tensors (not
>   nn.Parameters), the pop() is never reversed.  After the first sync
>   _parameters is permanently empty.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7155a0ba8a4f8b70d805a269d5507e032f26f7ad`.  There
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
{"case_id": "pytorch_rl__3804__7155a0b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
