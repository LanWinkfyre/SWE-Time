# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Stacked univariate distributions incompatible with PPOLoss and/or in composites with multivariate distributions

## Describe the bug

Some pytorch distributions like dirichlet are multivariate by nature. Some others like beta or gamma distributions are univariate by default.
However they can also be initialized with multivariate parameters which will cause torch to stack a number of independent univariate distributions.

This does not seem to work properly with the composite distribution and ppo loss in torchrl. Using such stacked univariate distributions leads to a shape mismatch when calculating the ppo loss as their `log_prob` and `log_weight` shapes are 4-dimensional while the natively multivariate distributions' log shapes are 3-dimensional.

Perhaps this issue only occurs when mixing stacked and native multivariate distributions but i have not tested this.

## To Reproduce

Create a probabilistic actor with a composite distribution using stacked univariate distributions.

A runnable example can be found here: https://github.com/rerz/rltest

I also tried splitting the stacked distributions into multiple ones with just one set of parameters but this still produces 4-dimensional log shapes.

It also contains a very unclean workaround in the forward method of `PPOLoss` which basically just removes this extra dimension and changes the reduction of the log weights to end up with a shape that is compatible with the advantage tensor.

## Expected behavior

I can use any distribution no matter if it is univariate or multivariate by default.

## System info

torchrl and tensordict from the current main branches.

## Reason and Possible fixes

A workaround can be found in the linked repo above. While the fix is unclean i believe to have found the root cause of the issue.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f0bba17126bd48f326043b008f838a3e0640b889`.  There
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
{"case_id": "pytorch_rl__2753__f0bba17",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
