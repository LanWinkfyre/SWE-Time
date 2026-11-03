# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Exclude models from idle unloading

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
<!-- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]  -->
No

**Describe the solution you'd like**
<!-- A clear and concise description of what you want to happen.  -->
I'd love the ability for some models to stay loaded to improve their responsiveness, while being able to unload others.
The ideal state would be to have a toggle or somewhere in the settings where we can list particular models that are excluded from unloading.

**Describe alternatives you've considered**
<!-- A clear and concise description of any alternative solutions or features you've considered.  -->
I've tried turning the idle unloading toggle off, and extending the time - but this has a negative effect when there are other models that I *do* want to be unloaded due to idle.

**Additional context**
<!-- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `062e0d0d00f47a037b8141c7beee69d610614b48`.  There
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
{"case_id": "mudler_LocalAI__9305__062e0d0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
