# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] TruncatedNormal rsample upcasts float16 inputs to float32

## Describe the bug

`TruncatedNormal.rsample()` upcasts `float16` parameters to `float32`, even when `loc`, `scale`, and truncation bounds all use `float16`. The same upcast occurs with the default scalar bounds. This can silently change the action dtype in mixed-precision policies.

## To Reproduce

```python
import torch
from torch.distributions import Normal
from torchrl.modules import TruncatedNormal

loc = torch.zeros(3, dtype=torch.float16)
scale = torch.ones_like(loc)
low = torch.full_like(loc, -1)
high = torch.full_like(loc, 1)

print(Normal(loc, scale).rsample().dtype)
print(TruncatedNormal(loc, scale).rsample().dtype)
print(TruncatedNormal(loc, scale, low=low, high=high).rsample().dtype)
```

Current output on pristine `main`:

```text
torch.float16
torch.float32
torch.float32
```

## Expected behavior

Both `TruncatedNormal` samples should preserve the promoted parameter/bound dtype and return `torch.float16` in this example, matching `torch.distributions.Normal`.

## System info

- Installed from a source checkout at `b0eab87eb17ac6a910758444e716992739e1440b`
- Python 3.13.3
- PyTorch 2.11.0+cu130
- TensorDict 0.13.0
- Windows 11

## Additional context

The problem affects both scalar and tensor bounds. `float32` and `float64` inputs already return samples in their expected dtype.

## Reason and Possible fixes

Two constructors introduce the upcast:

1. The public distribution converts scalar `low` and `high` without inheriting `loc.dtype`.
2. The standard truncated-normal sampler creates its inverse-CDF probabilities with `torch.empty(..., device=...)`, which uses the global default dtype rather than the normalized bound dtype.

Using `loc.dtype` for scalar bounds and a dtype-preserving tensor constructor for the probability samples fixes the issue while retaining normal PyTorch promotion for explicitly typed tensor bounds.

## Checklist

- [x] I have checked that there is no similar issue in the repo
- [x] I have read the documentation
- [x] I have provided a minimal working example to reproduce the bug
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b0eab87eb17ac6a910758444e716992739e1440b`.  There
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
{"case_id": "pytorch_rl__4136__b0eab87",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
