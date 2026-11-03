# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
parakeet can only be selected as an LLM and not as  a speech-to-text

**LocalAI version:**
latest docker, cloned yestarday

**Environment, CPU architecture, OS, and Version:**
```
Linux denis-pc 7.0.3-arch1-2 #1 SMP PREEMPT_DYNAMIC Fri, 01 May 2026 15:49:22 +0000 x86_64 GNU/Linux
```

**Describe the bug**
When creating a new speech-to-speech pipeline (icon of a phone) I cannot select parakeet in the speech-to-text field, only in LLM, but parakeet is not a LLM and nvidia clearly says it's a speech-to-text: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3

**To Reproduce**
Add the nvidia/parakeet-tdt-0.6b-v3 from huggingface, you will only be able to use it as an LLM (ofc it's not going to work)

**Expected behavior**
For speech-to-text to be usable as speech-to-text and not as an LLM

**Logs**
No need for logs

**Additional context**
No need for additional context
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e08492a2c3d73b7d65cb010682ad0d66fefbc8aa`.  There
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
{"case_id": "mudler_LocalAI__9718__e08492a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
