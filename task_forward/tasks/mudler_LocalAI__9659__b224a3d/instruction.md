# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Model Concurrency Matrix

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
I would like more control over which models can load concurrently. At the moment we can use "Max Active Backends" but that would allow 3 large models to load which may not fit.

**Describe the solution you'd like**
<!-- A clear and concise description of what you want to happen.  -->
Literally the matrix configuration from llama-swap: https://github.com/mostlygeek/llama-swap/issues/643 
This would allow specifying more complicated rules like "allow my zed prediciton model to run alongside anything but don't allow my two 120b models to run alongside eachother"

**Describe alternatives you've considered**
Max Active Backends - but has problem as mentioned above.

**Additional context**
<!-- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b224a3d931ebf6914f331ac71d041ff3416e67b8`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__9659__b224a3d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
