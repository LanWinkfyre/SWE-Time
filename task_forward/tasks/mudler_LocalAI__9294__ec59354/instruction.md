# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Renaming a model causes duplicates in the UI

**LocalAI version:**
LocalAI v4.1.3 (fdc9f7bf350b05942323f5f4b264480c7b67b51c)

**Environment, CPU architecture, OS, and Version:**
Docker, x64, Ubuntu, 24.04

**Describe the bug**
If you edit the model that is installed from the edit button under system, and hit save, it creates multiple models. If you delete the duplicates, it deletes all of it.

**To Reproduce**
1. Load any model from the gallery.
2. Go to system/system
3. Click edit on a model
4. Change the name in yaml
5. Hit save
6. Notice the duplicates

**Expected behavior**
The model name should be changed for all permutations that are created (i.e. for qwen asr there is qwen backend and vllm-omni, both should be updated)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ec5935421cd982f0dee8624dc0ef87ae78057b98`.  There
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
{"case_id": "mudler_LocalAI__9294__ec59354",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
