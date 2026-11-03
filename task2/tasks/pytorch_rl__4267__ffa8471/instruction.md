# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Performance] Compile the complete DreamerV3 learner step

### Problem

The DreamerV3 SOTA training path can compile the RSSM recurrence and replay the learner update through a CUDA graph, but the surrounding encoder, decoder, distribution heads, KL terms, imagination rollout, return normalization, and replay value loss remain eager. CUDA graph replay preserves that eager kernel topology, leaving the update exposed to launch overhead.

### Proposed change

Add an opt-in optimization.compile_train_step setting that compiles the complete learner forward and backward with TorchInductor before optional CUDA graph capture. Keep optimizer and target-network updates outside capture, keep the default eager behavior unchanged, and provide profiler-backed benchmark variants for kernel count, GPU time, and CPU launch time.

The compiled path should preserve input TensorDict keys and remain covered in the existing DreamerV3 objective and CUDA-graph tests.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ffa8471a3d49339e780fb8b7fbf83360e406b418`.  There
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
{"case_id": "pytorch_rl__4267__ffa8471",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
