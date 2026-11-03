# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Milvus Hybrid Search Returns Incorrect Chunks Regardless of Ranker Type

### System Info

`llama-stack-client==0.5.0`
`llama-stack==0.5.0`

### Information

- [ ] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

> [!note]
> Root cause analysis was run with `Opus 4.6`. The actual problem was found during RAG evaluation using [`ai4rag` ](https://github.com/IBM/ai4rag) library.

## Summary

`MilvusIndex.query_hybrid()` returns incorrect chunks when using `search_mode="hybrid"` via the `/v1/vector_stores/{id}/search` endpoint (the same is applicable for `/vector-io/query` as well). The same wrong chunk is returned regardless of the ranker type (weighted, RRF, or normalized) and regardless of alpha value (0 or 1). The returned chunk does not appear in standalone vector-only or keyword-only search results.

The root cause is that the hybrid search constructs its own `AnnSearchRequest` objects with **different parameters** than the standalone `query_vector()` and `query_keyword()` methods, producing a different candidate pool. Since this candidate pool is shared across all ranker types, every ranker returns the same incorrect result.

The bug was introduced in commit `e3928e6a` ("feat: Implement hybrid search in Milvus (#2644)") and is present in all versions since, including v0.5.2 and current main (HEAD).

### `ai4rag` results for RAG metrics using hybrid ranker
Several RAG Patterns were created using hybrid search mode only and vector search only. The mismatch can be seen in the scores achieved:

Non-hybrid:
<img width="989" height="490" alt="Image" src="https://github.com/user-attachments/assets/7b6d2046-f312-491f-84da-f4b81eba22bd" />

Hybrid:
<img width="989" height="490" alt="Image" src="https://github.com/user-attachments/assets/b34da47b-fde9-4963-8eaa-55c21a257340" />

---

## Affected Code

**Primary location:** `src/llama_stack/providers/remote/vector_io/milvus/milvus.py`, lines 201–256 (`MilvusIndex.query_hybrid`)

**Common ground (shared by all ranker types):** lines 218–228 — the `AnnSearchRequest` construction:

```python
search_requests = []
search_requests.append(
    AnnSearchRequest(data=[embedding.tolist()], anns_field="vector", param={"nprobe": 10}, limit=k)
)
search_requests.append(
    AnnSearchRequest(data=[query_string], anns_field="sparse", param={"drop_ratio_search": 0.2}, limit=k)
)
```

---

> [!note]
> financial documents from IBM's site were downloaded for the example presented above.
> Content was extracted to .txt and chunking using `RecusriveCharacterTextSplitter` from `LangChain` was conducted (chunk_size=1024).
> Documents:
> ```python
> documents_urls = [
>    "https://www.ibm.com/downloads/documents/us-en/12bb2f913a3ba1a2",
>    "https://www.ibm.com/downloads/documents/us-en/131cf8a39db327fd",
>    "https://www.ibm.com/downloads/documents/us-en/131cf87ab633199f",
>    "https://www.ibm.com/downloads/documents/us-en/1550f7eea8c0ded6",
>    "https://www.ibm.com/downloads/documents/us-en/10a9980400afd114",
>    "https://www.ibm.com/downloads/documents/us-en/10a9980468afdf4c",
>    "https://www.ibm.com/downloads/documents/us-en/10a9980400afd11c",
>    "https://www.ibm.com/downloads/documents/us-en/11ed3283ae56ec71"
>]

## Reproduction

```python
# After creating a vector store and inserting several documents with distinct content:

# 1. Keyword only — works correctly
kw = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="keyword", max_num_results=3
)

# 2. Vector only — works correctly
vec = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="vector", max_num_results=3
)

# 3. Hybrid with alpha=0 — SHOULD match keyword results, but returns chunk C
hybrid_kw = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="hybrid", max_num_results=3,
    ranking_options={"ranker": "weighted", "alpha": 0.0}
)

# 4. Hybrid with alpha=1 — SHOULD match vector results, but returns chunk C
hybrid_vec = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="hybrid", max_num_results=3,
    ranking_options={"ranker": "weighted", "alpha": 1.0}
)

# 5. Hybrid with RRF — also returns chunk C
hybrid_rrf = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="hybrid", max_num_results=3,
    ranking_options={"ranker": "rrf"}
)

# 6. Hybrid with normalized — also returns chunk C
hybrid_norm = client.vector_stores.search(
    vector_store_id=vs_id, query="my query",
    search_mode="hybrid", max_num_results=3,
    ranking_options={"ranker": "normalized"}
)
```

**Observed:** All hybrid calls (3–6) return the same chunk C, which does not appear in the standalone vector (2) or keyword (1) results.

**Expected:**
- `alpha=0.0` should return results identical to keyword-only search.
- `alpha=1.0` should return results identical to vector-only search.
- Intermediate alpha values should smoothly interpolate between the two.
- Different ranker types (weighted vs RRF) should produce different rankings.

---

## Root Cause Analysis

### Bug 1: Hybrid sub-searches use different parameters than standalone searches (common ground)

The `AnnSearchRequest` objects in `query_hybrid` are built with **different parameters** than the standalone `query_vector()` and `query_keyword()` methods. This is the common ground shared by all ranker types and explains why all rankers return the same incorrect chunk.

| Aspect | Standalone `query_vector` (line 133) | Hybrid dense `AnnSearchRequest` (line 221) |
|---|---|---|
| Score filtering | `{"params": {"radius": score_threshold}}` — filters at the Milvus search engine level | **Missing entirely** — no `radius` parameter |
| Effect | Only returns chunks with cosine similarity >= threshold | Returns top-k chunks regardless of similarity, including low/negative similarity chunks |

The standalone dense search tells Milvus: "only return results with cosine similarity >= `score_threshold`." The hybrid dense sub-search has no such constraint — it returns the top-k results by cosine distance regardless of how low the similarity is. This means the hybrid candidate pool includes chunks that standalone `query_vector` would never return.

Additionally, the post-filtering in `query_hybrid` (line 253) applies `score_threshold` to the **combined/weighted score** from the ranker, not the raw cosine similarity — a completely different scale:

```python
# This filters on COMBINED score, not raw cosine similarity
filtered_chunks = [chunk for chunk, score in zip(chunks, scores, strict=False) if score >= score_threshold]
filtered_scores = [score for score in scores if score >= score_threshold]
```

### Why this produces a chunk not found in either standalone search

Consider this scenario with 5 chunks and k=3, score_threshold=0.5:

| Chunk | Cosine similarity | BM25 score | Standalone dense top-3 (radius=0.5) | Standalone sparse top-3 |
|---|---|---|---|---|
| A | 0.95 | 0.1 | #1 | — |
| B | 0.80 | 0.3 | #2 | — |
| C | 0.40 | 2.0 | excluded (cosine < 0.5) | #3 |
| D | 0.10 | 5.0 | excluded | #1 |
| E | 0.05 | 4.0 | excluded | #2 |

Standalone `query_vector` (with `radius=0.5`): returns **{A, B}** only.

Standalone `query_keyword`: returns **{D, E, C}** (top-3 by BM25).

Hybrid dense `AnnSearchRequest` (**no radius filter**, just top-3 by cosine): returns **{A, B, C}** — chunk C sneaks in because it's in top-3 by raw cosine when there is no threshold.

Hybrid candidate pool (union of both sub-searches): **{A, B, C, D, E}**. Chunk C appears in **both** sub-searches, giving it a boost with ANY ranker:

- **RRF:** C is rank 3 in both → `1/(60+3) + 1/(60+3) = 0.032`. A is rank 1 in dense only → `1/(60+1) + 0 ≈ 0.016`. **C wins.**
- **Weighted (alpha=0.5):** C has moderate normalized scores in both dimensions, outranking chunks strong in only one.
- **Weighted (alpha=0 or 1):** Milvus's `WeightedRanker(norm_score=True)` normalizes scores over the hybrid sub-search results (not standalone results), producing unexpected rankings even at extreme alpha values.

### Bug 2: "normalized" reranker silently falls through to RRF

In `MilvusIndex.query_hybrid` (lines 230–235):

```python
if reranker_type == RERANKER_TYPE_WEIGHTED:
    rerank = WeightedRanker(alpha, 1 - alpha)
else:  # ← BOTH "rrf" AND "normalized" land here
    rerank = RRFRanker(impact_factor)
```

`RERANKER_TYPE_NORMALIZED` has no dedicated handling — it silently falls through to `RRFRanker`. This means "rrf" and "normalized" always produce identical results. (Note: `WeightedInMemoryAggregator.combine_search_results` in `vector_utils.py` has the same gap — this is a codebase-wide issue, not Milvus-specific.)

---

## Architectural Comparison Across Providers

| Provider | Hybrid approach | Calls same standalone methods? | Consistent with standalone by construction? |
|---|---|---|---|
| **sqlite_vec** | `query_vector()` + `query_keyword()` → `WeightedInMemoryAggregator` | Yes | Yes |
| **chroma** | Same as sqlite_vec | Yes | Yes |
| **pgvector** | Same as sqlite_vec | Yes | Yes |
| **oci** | Same as sqlite_vec | Yes | Yes |
| **milvus** | Native `hybrid_search` with separate `AnnSearchRequest` params | **No** | **No** |
| qdrant | Native `query_points` with filter | No | N/A (different design) |
| weaviate | Native `collection.query.hybrid()` | No | N/A (different design) |
| elasticsearch | Native retriever-based search | No | N/A (different design) |
| faiss | `raise NotImplementedError` | N/A | N/A |

The 4 providers using the in-memory approach (sqlite_vec, chroma, pgvector, oci) are **guaranteed consistent** with standalone searches because they call the exact same `query_vector()` and `query_keyword()` methods. The Milvus provider bypasses these methods entirely, using a separate code path with independently constructed `AnnSearchRequest` objects that have different parameters.

---

## Version Comparison

- **v0.5.2 vs HEAD (main):** The `milvus.py` code is **byte-for-byte identical**. The bug exists in both.
- **v0.6.x:** No 0.6.x release exists yet. Latest tag is `v0.5.3-dev`.
- **Introduced in:** commit `e3928e6a` ("feat: Implement hybrid search in Milvus (#2644)")

---

## Testing Gap

The existing integration test `test_openai_vector_store_search_with_weighted_ranker` only tests `alpha=0.7` and only asserts that:
1. Results exist
2. Scores are in descending order

There is **no test** verifying that:
- `alpha=0` hybrid results match keyword-only results
- `alpha=1` hybrid results match vector-only results
- Different ranker types produce different rankings
- Hybrid results are a subset of the union of standalone results

---

## Suggested Fix

Replace the native `hybrid_search` call with the same in-memory aggregation approach used by sqlite_vec, chroma, pgvector, and oci:

```python
async def query_hybrid(self, embedding, query_string, k, score_threshold,
                        reranker_type, reranker_params=None):
    # Use the SAME standalone search methods — guarantees consistency
    vector_response = await self.query_vector(embedding, k, score_threshold)
    keyword_response = await self.query_keyword(query_string, k, score_threshold)

    vector_scores = {
        c.chunk_id: s for c, s in zip(vector_response.chunks, vector_response.scores, strict=False)
    }
    keyword_scores = {
        c.chunk_id: s for c, s in zip(keyword_response.chunks, keyword_response.scores, strict=False)
    }

    combined = WeightedInMemoryAggregator.combine_search_results(
        vector_scores, keyword_scores, reranker_type, reranker_params or {}
    )

    sorted_items = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]
    filtered = [(did, s) for did, s in sorted_items if s >= score_threshold]

    chunk_map = {c.chunk_id: c for c in vector_response.chunks + keyword_response.chunks}
    chunks = [chunk_map[did] for did, _ in filtered if did in chunk_map]
    scores = [s for did, s in filtered if did in chunk_map]

    return QueryChunksResponse(chunks=chunks, scores=scores)
```

This guarantees:
- `alpha=0` matches keyword-only results
- `alpha=1` matches vector-only results
- Intermediate alpha values smoothly interpolate
- Consistent behavior with other providers

### Error logs

> [!CAUTION]
> There are no error logs generated. This is silent bug, that will reflect in the retrieved content quality.

### Expected behavior

1. Chunks retrieved should:
    - be the same when using `search_mode="hybrid"` and `search_mode="vector"` for `weighted` strategy and `alpha=1`
    - be the same when using `search_mode="hybrid"` and `search_mode="keyword"` for `weighted` strategy and `alpha=0`
    - differ in quality between search modes and ranker configurations (extends RAG patterns quality with more relevant content)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ad3b8032bcbb3211fd157f522e1d18761e0be11a`.  There
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
{"case_id": "ogx_ai_ogx__5112__ad3b803",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
