# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
ik_llama backend support

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
For local inference, partial offload is required for many models of reasonable quality. ik_llama.cpp is a fork of llama.cpp that has additional support for more modern and efficient quants and significantly better performance on modern hardware. I have personally been able to run significantly larger quants (2x size) at significantly better speeds (1.5x inference) using ik_llama, which completely redefines the capabilities of my local AI inference. LocalAI would become much more usable for local inference in my setup with the addition of an ik_llama cpp backend.
<!-- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]  -->

**Describe the solution you'd like**
Addition of ik_llama.cpp as a selectable backend.
<!-- A clear and concise description of what you want to happen.  -->

**Describe alternatives you've considered**
Considered using OobaBooga text generation webui but it's clearly not built for the same use case, can't run multiple models, and doesn't support auto load/unload. LocalAI is a true workhorse for multi-purpose local AI inference.
<!-- A clear and concise description of any alternative solutions or features you've considered.  -->

**Additional context**
N/A
<!-- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `151ad271f23d5037d59d64c2e6da3e98a2f82cc0`.  There
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
{"case_id": "mudler_LocalAI__9322__151ad27",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
