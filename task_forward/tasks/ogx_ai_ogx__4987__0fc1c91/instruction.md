# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
OpenResponses conformance: echo sampling parameters (temperature, top_p) as non-null in Responses API response

### 🤔 What is the technical debt you think should be addressed?

Part of #4986.

`temperature` and `top_p` are accepted as request inputs on the Responses API but are typed `float | None = None` in `OpenAIResponseObject`. The OpenResponses spec requires them as non-nullable numbers. Two changes are needed:

1. Give them non-null defaults in `OpenAIResponseObject`: `temperature: float = 1.0`, `top_p: float = 1.0`
2. Forward them from the streaming context in `_snapshot_response()` — they are available as `self.ctx.temperature` and `self.ctx.top_p` but are never set on the snapshot response object

**Files:**
- `src/llama_stack_api/openai_responses.py`
- `src/llama_stack/providers/inline/agents/meta_reference/responses/streaming.py`

### 💡 What is the benefit of addressing this technical debt?

OpenAI Responses API parity is crucial for LLS adoption. This is one of the gaps blocking the OpenResponses conformance suite from passing.

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0fc1c91728c260612e1cbecf74be42cb96837850`.  There
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
{"case_id": "ogx_ai_ogx__4987__0fc1c91",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
