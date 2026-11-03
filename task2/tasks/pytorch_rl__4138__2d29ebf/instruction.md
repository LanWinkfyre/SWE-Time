# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
`examples/rlhf/train.py` uses deprecated `torch.cuda.amp.GradScaler` — last torch.cuda.amp reference in the repo

## Summary

[examples/rlhf/train.py:96](https://github.com/pytorch/rl/blob/main/examples/rlhf/train.py#L96):

```python
scaler = torch.cuda.amp.GradScaler(enabled=(dtype == "float16"))
```

`torch.cuda.amp.GradScaler` has been deprecated since torch 2.3 (and `torch.cuda.amp.autocast` since 2.4); both are scheduled for removal. On torch 2.4+ this line emits a `FutureWarning`; after removal it will raise `AttributeError`.

This appears to be the **last `torch.cuda.amp` reference in the repository**:

- The same example's autocasting already goes through the new API — [examples/rlhf/utils.py:256](https://github.com/pytorch/rl/blob/main/examples/rlhf/utils.py#L256) returns `torch.amp.autocast(device_type="cuda", ...)`.
- The library core (`torchrl/`) already uses `torch.amp.*` throughout (e.g. `torchrl/modules/models/model_based.py`, `model_based_v3.py`, `sota-implementations/expert-iteration`).

## How to reproduce

```bash
pip install torch>=2.4  # the repo's floor is torch>=2.1.0 (pyproject.toml)
python -W error::FutureWarning examples/rlhf/train.py --help  # or any run reaching line 96
```

```
FutureWarning: torch.cuda.amp.GradScaler is deprecated. Please use torch.amp.GradScaler('cuda', ...)
```

(Verified on torch 2.11: the warning fires at construction; `warnings.simplefilter("error", FutureWarning)` turns it into an error.)

## Request

Migrate line 96 to the `torch.amp` API:

```python
scaler = torch.amp.GradScaler("cuda", enabled=(dtype == "float16"))
```

`torch.amp.GradScaler` exists since torch 2.3. The declared floor is `torch>=2.1.0`, but the library core already requires `torch.amp` in practice, so this does not raise the effective minimum. The fix is one line, aligns the example with the rest of the repo, and removes the warning every fp16 RLHF run emits.

## Suggested fix

Single-line change in `examples/rlhf/train.py`:

```diff
- scaler = torch.cuda.amp.GradScaler(enabled=(dtype == "float16"))
+ scaler = torch.amp.GradScaler("cuda", enabled=(dtype == "float16"))
```

## References

- PyTorch deprecation: `torch.cuda.amp.GradScaler` deprecated since 2.3, `torch.cuda.amp.autocast` since 2.4 ([PyTorch release notes](https://github.com/pytorch/pytorch/releases)); `torch.amp` is the replacement namespace.
- Same migration precedent: [ultralytics/yolov5#13244](https://github.com/ultralytics/yolov5/pull/13244), [huggingface/lerobot#3167](https://github.com/huggingface/lerobot/pull/3167).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2d29ebf3ec5c51083a0f436060e80d1286e3e33e`.  There
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
{"case_id": "pytorch_rl__4138__2d29ebf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
