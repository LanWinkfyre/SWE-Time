# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Documentation about recommended use of .train() and .eval()

## Motivation

The ClipPPOLoss documentation says "it is highly recommended to keep your model in eval mode" and there is a [ConsistentDropoutModule](https://docs.pytorch.org/rl/0.7/reference/generated/torchrl.modules.ConsistentDropoutModule.html#torchrl.modules.ConsistentDropoutModule) which makes me think that having dropout in normal nn.Modules is not recommended?

I just happened to stumble across this information in the docs, it is not mentioned in any of the tutorials that I have read.

## Solution

- Add a section in the [Getting started with model optimization](https://docs.pytorch.org/rl/stable/tutorials/getting-started-2.html) page that explains whether .eval() should be used consistently or not.
- Use .eval() consistently in the tutorials, notably the [PPO one](https://docs.pytorch.org/rl/stable/tutorials/coding_ppo.html).

## Checklist

- [X] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `da6120e48f565857629087f3b8399c7148b8f9d5`.  There
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
{"case_id": "pytorch_rl__3140__da6120e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
