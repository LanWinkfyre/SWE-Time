# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
test_openai_completion_guided_choice fails with vLLM v0.15.0

`test_openai_completion_guided_choice` fails when running against vLLM v0.15.0 (and any version >= v0.12.0).

The test sends `guided_choice` via `extra_body`, but vLLM removed the `guided_*` API fields in v0.12.0 ([vllm-project/vllm#29326](https://github.com/vllm-project/vllm/pull/29326)). The server silently ignores the unrecognized field and generates unconstrained output, causing the assertion to fail.

**What happens:**

The test sends `extra_body={"guided_choice": ["joy", "sadness"]}`. vLLM logs a warning (`The following fields were present in the request but ignored: {'guided_choice'}`) and returns unconstrained text instead of one of the expected choices.

**What should happen:**

The test should use the replacement API `extra_body={"structured_outputs": {"choice": ["joy", "sadness"]}}` so that vLLM applies constrained decoding and returns one of the expected choices.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c19a77d4a05907fef2f1d58752ad5d7116310888`.  There
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
{"case_id": "ogx_ai_ogx__4984__c19a77d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
