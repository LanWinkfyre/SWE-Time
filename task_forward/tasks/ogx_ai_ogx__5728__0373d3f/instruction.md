# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
feat: add pluggable chunk classifier API for post-retrieval filtering in RAG

## Problem

Vector search ranks by embedding similarity, but similarity ≠ usefulness for answering a query. Common failure modes in RAG:

- Semantically similar but unhelpful chunks (topically related boilerplate)
- High similarity, low information density
- Ranking quality degrades with corpus size (top-K increasingly noisy)

Existing rerankers (RRF, weighted, neural) re-score by relevance but don't filter for chunk *quality* — whether a chunk is well-formed, complete, non-redundant, and likely to produce a correct answer.

## Proposal

Add a chunk classifier that runs after retrieval and reranking, filtering or re-scoring chunks before they enter the LLM context:

```
Query → Embedding → Vector Search → Metadata Filter → Reranker → [Chunk Classifier] → LLM
```

### Option A: New parameter on Search API

Add an optional `chunk_classifier` field to the search endpoint:

```json
POST /v1/vector_stores/{id}/search
{
  "query": "...",
  "chunk_classifier": {
    "model": "my-classifier",
    "threshold": 0.7,
    "strategy": "filter"
  }
}
```

Minimal API change, but limited flexibility.

### Option B: New provider type — `chunk_classifier`

Register as a pluggable provider alongside inference and vector_io:

```yaml
providers:
  chunk_classifier:
    - provider_id: quality-filter
      provider_type: inline::transformer-classifier
      config:
        model: my-org/chunk-quality-classifier
        threshold: 0.7
    - provider_id: llm-judge
      provider_type: inline::llm-as-judge
      config:
        model: gpt-4o-mini
```

Enables multiple implementations:
- `inline::transformer-classifier` — fine-tuned BERT/DeBERTa
- `inline::llm-as-judge` — LLM-based chunk scoring
- `inline::rule-based` — heuristic filters (length, density, dedup)
- `remote::custom` — external classifier service

### Option C: New reranker type

Add a `"classifier"` value to the existing `ranker` parameter. Zero API changes but conflates two distinct concerns (ranking vs filtering).

## Recommendation

**Option B** provides the most flexibility — it follows OGX's existing provider pattern, allows independent evolution of classifier implementations, and enables users to compose classifiers with any reranker and any vector backend. The classifier is orthogonal to retrieval, just as the reranker is orthogonal to the vector store.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0373d3fda307c709756c7d9813040fecfc4236c4`.  There
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
{"case_id": "ogx_ai_ogx__5728__0373d3f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
