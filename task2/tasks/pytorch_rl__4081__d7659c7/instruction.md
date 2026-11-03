# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] DistillationLoss misses empty sequences in multidimensional batches

## Describe the bug

`DistillationLoss` checks whether each scored sequence has at least one selected token, but the check collapses every remaining dimension of each outer-batch slice. For a multidimensional TensorDict batch, an empty sequence therefore passes whenever another sequence in the same slice has a selected token.

The loss then silently returns zero for that sequence because sequence-length normalization clamps its zero denominator. This is particularly relevant to grouped LLM batches such as `[prompts, generations]`.

## To reproduce

On current `main` (`d7659c781a55f7680a025f16015064b0a8169344`):

```python
import torch
from tensordict import TensorDict
from tensordict.nn import TensorDictModule
from torchrl.objectives.llm import DistillationLoss

mask = torch.ones(2, 2, 3, dtype=torch.bool)
mask[0, 1] = False  # one complete sequence has no selected tokens
student_log_probs = torch.full((2, 2, 3), -1.0)
data = TensorDict(
    {
        (history, full): student_log_probs,
        (masks, all_attention_mask): mask,
        (masks, all_assistant_mask): mask,
        (next, teacher_log_probs, full): torch.full((2, 2, 3), -2.0),
    },
    batch_size=(2, 2),
)
student = TensorDictModule(
    torch.nn.Identity(),
    in_keys=[(history, full)],
    out_keys=[(log_probs, full)],
)

print(DistillationLoss(actor_network=student, reduction=none)(data).loss_distill)
```

Current output:

```text
tensor([[0.3679, 0.0000],
        [0.3679, 0.3679]])
```

## Expected behavior

Raise the existing `ValueError` saying that some sequences have no tokens selected. That is already the intended behavior for a one-dimensional batch; it should apply independently to every sequence in any supported TensorDict batch shape.

## Reason and possible fix

`forward` currently uses `not mask.any()` while iterating over the outer batch dimension. It should reduce only the token dimension, then check whether any resulting per-sequence flag is false. The token dimension is already encoded by the existing reductions as `tensordict.ndim - 1` after the outer iteration.

## System info

- Source checkout at `d7659c781a55f7680a025f16015064b0a8169344`
- TensorDict 0.13.0
- PyTorch 2.11.0+cu130 (CPU reproduction)
- Python 3.13.3
- Windows 11

## Checklist

- [x] I checked issues, pull requests, commits, and the introducing PR #4038 for similar reports.
- [x] I read the DistillationLoss documentation.
- [x] I provided a minimal working example.

## AI assistance disclosure

I used OpenAI Codex to help inspect the implementation, construct and run the reproduction, search for duplicates, and draft this report. I reviewed the reproduced behavior and report before submission.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d7659c781a55f7680a025f16015064b0a8169344`.  There
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
{"case_id": "pytorch_rl__4081__d7659c7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
