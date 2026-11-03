# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
feat(bedrock): auto-discover models via ListFoundationModels

## Summary

The Bedrock inference provider's `list_provider_model_ids()` currently returns `[]` because Bedrock's OpenAI-compatible Mantle endpoint has no `/v1/models` route. This forces users to pre-register every model via `registered_resources` in their config.yaml.

All other major providers (Anthropic, VertexAI, OpenAI, vLLM) auto-discover models at startup. Bedrock should too.

## Proposed solution

Use the AWS `bedrock:ListFoundationModels` API (via boto3) to populate the model list when SigV4 auth is active. The existing `create_bedrock_client()` utility in `ogx/providers/utils/bedrock/client.py` already handles all credential modes (static keys, role assumption, web identity, profiles).

### Implementation

Single file change in `src/ogx/providers/remote/inference/bedrock/bedrock.py`:

1. In `initialize()`, create a boto3 `bedrock` service client (not `bedrock-runtime`) via `create_bedrock_client(config, "bedrock")` — same pattern the safety provider already uses
2. Replace `list_provider_model_ids()` to call `list_foundation_models(byInferenceType="ON_DEMAND")`, filter to `ACTIVE` lifecycle status, return model IDs
3. Run via `asyncio.to_thread()` since boto3 is synchronous
4. Fall back to `[]` for bearer-token-only deployments (no boto3 client available)

### Sketch

```python
async def list_provider_model_ids(self) -> Iterable[str]:
    if self._bedrock_client is None:
        return []
    response = await asyncio.to_thread(
        self._bedrock_client.list_foundation_models,
        byInferenceType="ON_DEMAND",
    )
    return [
        m["modelId"]
        for m in response.get("modelSummaries", [])
        if m.get("modelLifecycleStatus") == "ACTIVE"
    ]
```

### IAM requirement

The IAM role/user needs the `bedrock:ListFoundationModels` permission. This is a read-only action on a different service (`bedrock`) than the inference calls (`bedrock-runtime`).

## Context

- Related: #5230 (broader Bedrock Converse API support)
- The [SigV4 auth blog post](https://ogx-ai.github.io/blog/ogx-bedrock-aws-auth) documents the `registered_resources` workaround
- The `create_bedrock_client()` utility is already used by the safety provider (`remote/safety/bedrock/bedrock.py:38`)

I'd like to take this on — happy to submit a PR.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `189de747dca111f247d96404beb1e81e03c655a3`.  There
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
{"case_id": "ogx_ai_ogx__6312__189de74",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
