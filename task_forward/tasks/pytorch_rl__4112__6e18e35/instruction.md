# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Sparse MaskedCategorical mode uses compressed indices

## Describe the bug

`MaskedCategorical` with sparse `indices` reports its mode in the compressed index space rather than the original action space. The result can be an action excluded by the mask, and `log_prob(dist.mode)` can consequently be `-inf`. `MaskedOneHotCategorical` has the same mapping problem and also returns a one-hot vector whose width is the number of valid indices rather than the original number of actions.

## To Reproduce

```python
import torch
from torchrl.modules.distributions import MaskedCategorical, MaskedOneHotCategorical

logits = torch.tensor([0.0, 1.0, 10.0, 2.0])
indices = torch.tensor([0, 2])

for cls in (MaskedCategorical, MaskedOneHotCategorical):
    dist = cls(logits=logits, indices=indices)
    print(cls.__name__, dist.mode, dist.log_prob(dist.mode), dist.sample())
```

On current `main` (`6e18e35b2`), this prints a categorical mode of `1` with log-probability `-inf`, while samples correctly map back to action `2`. The one-hot mode is `[0, 1]` instead of `[0, 0, 1, 0]`.

## Expected behavior

`mode` and `deterministic_sample` should use the same original action space as `sample`: `2` for `MaskedCategorical` and `[0, 0, 1, 0]` for `MaskedOneHotCategorical`. Their log-probabilities should be finite.

## System info

- Installed from source at `6e18e35b2`
- Python 3.13.3
- PyTorch 2.11.0+cu130 (CPU reproduction)
- Windows 11

## Reason and Possible fixes

Sparse construction gathers logits to the valid-index subset. The inherited categorical mode is therefore an offset into that gathered tensor. `sample()` maps this offset back through `self._mask`, but the mode properties do not. Mapping the categorical mode through the sparse indices, then creating the one-hot result with `num_samples` classes, restores consistency.

## Checklist

- [x] I have checked that there is no similar issue in the repo
- [x] I have read the documentation
- [x] I have provided a minimal working example to reproduce the bug

## Generative-tool disclosure

I used OpenAI Codex to assist with repository auditing, reproduction, duplicate searches, and drafting this report. I reviewed the reproduced behavior and proposed scope.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6e18e35b2c68be1a56afebfb0676d217925114cd`.  There
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
{"case_id": "pytorch_rl__4112__6e18e35",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
