# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Altering LLM responses post fact

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
<!-- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]  -->
Sometimes the answers a LLM gives would be good except for a few details. I would like for the ability to alter those answers
**Describe the solution you'd like**
A button under the answer and the prompt that when clicked open a textbox to change the answer. Same under the prompt, with at least a button to save the change without sending a new request
<!-- A clear and concise description of what you want to happen.  -->

**Describe alternatives you've considered**
Exxporting the answer, editing it in a text editor and then uploading it to a new chat could work too

**Additional context**
<!-- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b13c429b3bf8ffaa211bd01da60e71bb03572041`.  There
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
{"case_id": "mudler_LocalAI__10805__b13c429",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
