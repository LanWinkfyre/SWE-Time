# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Vector store creation ignores model's embedding_dimension metadata, defaults to 768

## Bug

When creating a vector store via `POST /v1/vector_stores` with an `embedding_model` but without an explicit `embedding_dimension`, the store is initialized with 768 dimensions regardless of the model's registered `embedding_dimension` metadata. This causes an `Embedding dimension mismatch` error on file ingestion for any model that doesn't output 768-dim vectors.

## Reproduction

1. Register an embedding model with `embedding_dimension: 384` in the LlamaStack config:

```yaml
models:
  - metadata:
      embedding_dimension: 384
    model_id: all-MiniLM-L6-v2
    provider_id: vllm-embedding
    provider_model_id: sentence-transformers/all-MiniLM-L6-v2
    model_type: embedding
```

2. Create a vector store referencing that model:

```bash
curl -X POST /v1/vector_stores \
  -H "Content-Type: application/json" \
  -d '{"name": "my-store", "embedding_model": "all-MiniLM-L6-v2"}'
```

3. Upload and attach a file to the store.

4. File ingestion fails:

```
ValueError: Embedding dimension mismatch. Expected 768, got 384
```

## Root cause

In `llama_stack/providers/utils/memory/openai_vector_store_mixin.py`, line 56:

```python
EMBEDDING_DIMENSION = 768
```

When `embedding_model` is provided in `extra_body` but `embedding_dimension` is not, line ~390 applies the hardcoded default:

```python
embedding_dimension = extra_body.get("embedding_dimension", EMBEDDING_DIMENSION)
```

This sets `embedding_dimension = 768`, which prevents the lookup at line ~407 from ever executing:

```python
elif embedding_dimension is None:
    embedding_dimension = await self._get_embedding_dimension_for_model(embedding_model)
```

## Suggested fix

Change the default from `EMBEDDING_DIMENSION` to `None` so the model metadata lookup runs when dimension is not explicitly provided:

```python
embedding_dimension = extra_body.get("embedding_dimension")  # was: extra_body.get("embedding_dimension", EMBEDDING_DIMENSION)
```

The `_get_embedding_dimension_for_model` function already exists and correctly reads the registered model's metadata. It just never gets called because the default masks it.

## Workaround

Pass `embedding_dimension` explicitly in the create request:

```json
{"name": "my-store", "embedding_model": "all-MiniLM-L6-v2", "embedding_dimension": 384}
```

## Environment

- LlamaStack version: `0.3.0rc3+rhai0`
- Vector IO provider: `inline::faiss`
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) served via vLLM
- Platform: OpenShift 4.20 with LlamaStack operator 0.4.0
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bc8f92ac18b5ef39f5a119774d79a13ee8230bf6`.  There
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
{"case_id": "ogx_ai_ogx__5585__bc8f92a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
