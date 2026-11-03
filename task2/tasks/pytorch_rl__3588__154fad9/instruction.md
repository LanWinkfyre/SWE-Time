# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] New Tutorial - Trajectory Assembly internals in the TorchRL Collectors

## Feature request: Add tutorial on trajectory assembly internals in TorchRL collectors

### Summary
Add a tutorial that explains how collector batches are turned into complete trajectories, padded, and masked, with a focus on:
- `split_trajectories(...)`
- `_traj_ingest(...)`
- `_traj_emit(...)`
- done/terminated boundary handling
- nested vs padded trajectory outputs

### Motivation
Users training recurrent or sequence-based policies often need to understand:
- why trajectories are split across collector batches,
- how partial trajectories are buffered and reassembled,
- how `("collector", "traj_ids")` and `("collector", "mask")` are used,
- when to use `as_nested=True` vs zero-padded tensors.

Current docs show usage, but not enough collector-internal dataflow.

### Proposed tutorial title
**TorchRL Collectors Deep Dive: Trajectory IDs, Partial Chunks, and Emission**

### Learning goals
By the end, users should be able to:
1. Build a mental model of collector chunking and trajectory boundaries.
2. Use `split_trajectories` correctly with `trajectory_key` / `done_key`.
3. Understand and debug `trajs_per_batch`-style workflows.
4. Choose between padded and nested outputs.

### Proposed outline
1. Create synthetic batched collector output with `traj_ids` and done signals.
2. Walk through `split_trajectories` behavior in common and edge cases.
3. Demonstrate partial trajectory buffering across multiple batches via `_traj_ingest`.
4. Emit fixed number of full trajectories with `_traj_emit`.
5. Show mask semantics and downstream model usage.
6. Performance notes for `as_nested=True` and layout choices.

### Acceptance criteria
- Includes end-to-end runnable code.
- Includes one edge case where a trajectory spans multiple collector iterations.
- Includes visual check of `mask`, `traj_ids`, and final padded batch shape.
- Includes troubleshooting section for missing `("collector", "traj_ids")`.

### Nice-to-have
- Benchmark snippet comparing padded vs nested output for sequence models.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `154fad9798d1af711d8899f01c947dac140736ca`.  There
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
{"case_id": "pytorch_rl__3588__154fad9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
