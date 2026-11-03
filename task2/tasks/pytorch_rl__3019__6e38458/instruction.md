# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Having configurable `frames_per_batch_worker` on `_MultiDataCollector`

## Motivation

Currently, the `frames_per_batch` parameter is uniformly applied across all workers, which can lead to suboptimal utilisation of computational resources when dealing with heterogeneous environments per worker. One might want to build a batch with different fraction of the batch's frames per worker to account for specifics in the environments.

## Solution

I propose that `_MultiDataCollector` exposes both `frames_per_batch: int | None` and `frames_per_batch_worker: Sequence[int] | None`. These should be mutually exclusive and in the case were `frames_per_batch_worker` is provided, `frames_per_batch`can be computed as `sum(frames_per_batch_worker)`.

I'll propose a PR in this direction.

## Alternatives

An alternative would be to implement a new Collector handling this. This will lead to a load of code duplication for little to gain.

## Additional context

-

## Checklist

- [ ] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6e3845813c84e4377cbd92a60dbe2eca91732d6d`.  There
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
{"case_id": "pytorch_rl__3019__6e38458",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
