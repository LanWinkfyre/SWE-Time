# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
Setting `5.3` and `9` to `bits` argument of `RandomPosterize()` gets an indirect error message

### 🐛 Describe the bug

Setting `5.3` and `9` to `bits` argument of [RandomPosterize()](https://pytorch.org/vision/main/generated/torchvision.transforms.v2.RandomPosterize.html) gets the indirect error message as shown below:

```python
from torchvision.datasets import OxfordIIITPet
from torchvision.transforms.v2 import RandomPosterize

my_data1 = OxfordIIITPet(
    root="data",                 # ↓↓↓
    transform=RandomPosterize(bits=5.3)
)

my_data2 = OxfordIIITPet(
    root="data",                 # ↓
    transform=RandomPosterize(bits=9)
)

my_data1[0] # Error
my_data2[0] # Error
```

> TypeError: bad operand type for unary ~: 'float'

> TypeError: bad operand type for unary ~: 'float'

So, they should be something direct like below respectively:

> TypeError: `bits` must be `int`

> ValueError: `bits` must be [0, 8]



### Versions

```python
import torchvision

torchvision.__version__ # '0.20.1'
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8a06122218e54993e3c32523a904e847ff20b39c`.  There
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
{"case_id": "pytorch_vision__8910__8a06122",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
