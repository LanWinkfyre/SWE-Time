# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
CUDA-only VecNorm cases are excluded from GPU CI

### Problem

Two CUDA-specific cases in `test/transforms/test_normalization.py` use CUDA availability skip markers but do not carry the `gpu` marker:

- `TestVecNormV2.test_shared_stats_stay_shared_on_device_move[cuda]`
- `TestVecNormV2.test_vecnorm_gpu_device_handling[cuda]`

The unified Linux workflow partitions tests with `-m "not gpu"` on CPU runners and `-m gpu` on GPU runners. The CPU jobs collect these cases and skip them because CUDA is unavailable. The GPU jobs deselect them before execution because the cases lack the `gpu` marker. As a result, neither CUDA regression runs in normal Linux CI.

### Reproduction

On current `main`:

```text
pytest test/transforms/test_normalization.py -m gpu --collect-only -q
no tests collected (35 deselected)
```

### Expected behavior

The CUDA parameters should carry `pytest.mark.gpu`, while the MPS parameters should remain outside the CUDA partition. GPU collection should then select the two CUDA cases without moving the MPS cases out of their existing test lane.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `23746b7eb7a9b9c16f68aaab67dc7c22cc547bff`.  There
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
{"case_id": "pytorch_rl__4156__23746b7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
