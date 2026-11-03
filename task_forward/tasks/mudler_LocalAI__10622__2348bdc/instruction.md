# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Model default reasoning_effort: none does not work

**LocalAI version:**
4.5.6

**Environment, CPU architecture, OS, and Version:**
Linux marvin 7.0.14-arch1-1 #1 SMP PREEMPT_DYNAMIC Sat, 27 Jun 2026 16:15:10 +0000 x86_64 GNU/Linux

**Describe the bug**
Setting `reasoning_effort: none` without explicitly setting `reasoning.disable` does not have the desired effect.

**To Reproduce**
Set `reasoning_effort: none` in a model.yaml without explicitly setting any value for `reasoning.disable`.

Make the first request to a model with no reasoning effort or explicit `reasoning_effort = "none"` param in the request, and `reasoning.disable` [gets set to true](https://github.com/mudler/LocalAI/blob/v4.5.6/core/config/model_config.go#L696).

This would work as intended, except that it still needs to [probe for the media marker, which then updates](https://github.com/mudler/LocalAI/blob/v4.5.6/core/backend/llm.go#L126-L139) `reasoning.disable` to true in memory, and is returned with that value for the next request. The probe does not actually change this value. The post-probe UpdateModelConfig saves the result from ApplyReasoningEffort, which should not be connected.

One the next request, the reasoning effort gets passed through, but now `reasoning.disable` is set to true (as if set by the operator) so the `reasoning_effort` param has no effect.

**Expected behavior**
If I set reasoning_effort: none in model.yaml and do not set any value for reasoning.disable, I expect none to be the default, but to retain the ability to request extra thinking via the reasoning_effort request param.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2348bdc16d244518881eba38e0c79c51efc46a0e`.  There
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
{"case_id": "mudler_LocalAI__10622__2348bdc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
