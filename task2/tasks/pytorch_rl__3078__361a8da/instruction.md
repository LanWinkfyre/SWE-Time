# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] `MaskedCategorical`'s `use_cross_entropy` is not compatible with previously working shapes

## Describe the bug

The update to `torchrl>=0.9.0` switched `MaskedCategorical`'s default argument from `use_cross_entropy=False` to `use_cross_entropy=True`. This is not compatible with shapes that were previously compatible

## To Reproduce

```python
from functools import partial

import pytest
import torch
from torchrl.modules import MaskedCategorical

def test__MaskedCategorical__fails() -> None:
    """Checks the presence of a shape-related bug when computing log probabilities."""
    batch_size = (2, 3, 4) # typical tensor shape [N, T, A] ie, (batch_size, sequence_length, num_agents)

    masks = torch.tensor([[True, False, True, False, True]], dtype=torch.bool)
    logits = torch.randn((5,)).expand(*batch_size, -1)  # has shape [N, T, A, num_actions] during train
    action = torch.tensor(0, dtype=torch.long).expand(*batch_size)  # has shape [N, T, A] during train

    cat = MaskedCategorical(logits=logits, mask=masks)
    with pytest.raises(RuntimeError, match="size mismatch"):
        cat.log_prob(action)

    fixed_cat = MaskedCategorical(logits=logits, mask=masks, use_cross_entropy=False)
    fixed_cat.log_prob(action)
```

I have tried different shapes for actions/masks to see if I could make it work, but I had no success.

## Checklist

- [X] I have checked that there is no similar issue in the repo
- [X] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/)
- [X] I have provided a minimal working example to reproduce the bug
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `361a8da6edc77979e17409cf19396230d18c18a9`.  There
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
{"case_id": "pytorch_rl__3078__361a8da",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
