# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Milvus: query_chunks crashes on empty vector store; openai_search silently swallows the error

### System Info

- ogx version: 1.0.0
- Python: 3.12
- pymilvus: 2.6.9
- Affects both `inline::milvus` and `remote::milvus`

### Information

- [x] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

Querying a Milvus vector store that has no data inserted yet crashes with `MilvusException: collection does not exist` (HTTP 500). The same operation on `inline::faiss` returns `{"chunks":[],"scores":[]}` (HTTP 200) as expected.

The OpenAI-compatible `/v1/vector_stores/{id}/search` endpoint hits the same crash internally but a broad `except Exception` handler silently catches it and returns `{"data":[]}` with HTTP 200 — hiding the failure completely.

### Root cause

Milvus collections are lazily created on first `insert_chunks`. When `query_chunks` is called before any insert, `MilvusIndex.query_vector` calls `self.client.search` on a non-existent collection, which throws `MilvusException(code=100, message=collection '...' does not exist)`.

The `openai_search_vector_store` method in `openai_vector_store_mixin.py` wraps the call in:
```python
except Exception as e:
    logger.error("Error searching vector store", ...)
    return VectorStoreSearchResponsePage(..., data=[], ...)
```
This swallows the error and returns an empty response, making it impossible to detect the failure from the client side.

### Steps to reproduce

```bash
# Start the starter distribution with both faiss and milvus providers

# 1. Create empty vector stores
FAISS_VS=$(curl -s http://localhost:8321/v1/vector_stores \
  -H "Content-Type: application/json" \
  -d '{"name":"faiss-empty","provider_id":"faiss","metadata":{"embedding_model":"sentence-transformers/nomic-ai/nomic-embed-text-v1.5","embedding_dimension":"768"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

MILVUS_VS=$(curl -s http://localhost:8321/v1/vector_stores \
  -H "Content-Type: application/json" \
  -d '{"name":"milvus-empty","provider_id":"milvus","metadata":{"embedding_model":"sentence-transformers/nomic-ai/nomic-embed-text-v1.5","embedding_dimension":"768"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Query empty faiss — works
curl -s http://localhost:8321/v1/vector-io/query \
  -H "Content-Type: application/json" \
  -d "{\"vector_store_id\":\"$FAISS_VS\",\"query\":\"test\"}"
# Returns: {"chunks":[],"scores":[]}

# 3. Query empty milvus — crashes
curl -s http://localhost:8321/v1/vector-io/query \
  -H "Content-Type: application/json" \
  -d "{\"vector_store_id\":\"$MILVUS_VS\",\"query\":\"test\"}"
# Returns: {"error":{"message":"Internal server error: An unexpected error occurred."}}

# 4. OpenAI search on empty milvus — silently fails
curl -s "http://localhost:8321/v1/vector_stores/$MILVUS_VS/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"test","max_num_results":3}'
# Returns: {"data":[],...} (HTTP 200 — error is swallowed)
# Server log shows: MilvusException: collection '...' does not exist
```

### Expected behavior

Querying an empty Milvus vector store should return `{"chunks":[],"scores":[]}` with HTTP 200, consistent with faiss and other providers. The OpenAI search endpoint should not silently swallow provider errors.

### Suggested fix

In `MilvusIndex.query_vector` (or the caller), check `has_collection` before searching, and return empty results if the collection doesn't exist yet:

```python
if not await asyncio.to_thread(self.client.has_collection, self.collection_name):
    return QueryChunksResponse(chunks=[], scores=[])
```

### Why CI doesn't catch this

The upstream integration tests always follow a `create → insert → query` sequence. The collection is created during `insert`, so the query never hits a non-existent collection. There are no tests for querying an empty/newly-created vector store.

### Related issues

- #5209 — kvstore persistence (separate but related Milvus provider bug)
- #5119 — collection naming convention
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `479af786e0bf42f9ba59e6b237f5f74a3481014f`.  There
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
{"case_id": "ogx_ai_ogx__5833__479af78",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
