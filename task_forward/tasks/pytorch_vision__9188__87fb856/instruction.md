# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
InterpolationMode.NEAREST_EXACT and InterpolationMode.NEAREST are the same for tv_tensors.Mask

### 🐛 Describe the bug

When resizing tensor wrapped in tv_tensors.Mask interpolation mode NEAREST_EXACT is changed to NEAREST

```python
import torch
import torch.nn.functional as F
import torchvision.transforms.v2 as T
import torchvision.transforms.v2.functional as TF
from torchvision import tv_tensors


def compare(mask, size):
    mask_nearest = TF.resize(mask, size=size, interpolation=T.InterpolationMode.NEAREST)
    mask_nearest_exact = TF.resize(mask, size=size, interpolation=T.InterpolationMode.NEAREST_EXACT)
    mask_nearest_interpolate = F.interpolate(mask.unsqueeze(0), size=size, mode='nearest').squeeze(0)
    mask_nearest_exact_interpolate = F.interpolate(mask.unsqueeze(0), size=size, mode='nearest-exact').squeeze(0)
    
    print(torch.equal(mask_nearest, mask_nearest_exact))
    print(torch.equal(mask_nearest_interpolate, mask_nearest_exact_interpolate))
    print(torch.equal(mask_nearest, mask_nearest_interpolate))
    print(torch.equal(mask_nearest_exact, mask_nearest_exact_interpolate))
    

height = 64
width = 64
new_height = 16
new_width = 16
mask = torch.randint(low=0, high=2, size=(1, height, width)).float()

compare(mask, (new_height, new_width))
print()

mask = tv_tensors.Mask(mask)
compare(mask, (new_height, new_width))
```

```
False
False
True
True

True
False
True
False
```

### Versions

torch = "2.8.0"
torchvision = "0.23.0"
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `87fb856a8a9abe511bb98772d1202d08b1fe2933`.  There
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
{"case_id": "pytorch_vision__9188__87fb856",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
