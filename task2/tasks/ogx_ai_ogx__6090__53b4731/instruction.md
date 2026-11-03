# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
inline::milvus vector query fails with KeyError: 'chunk_content' when using milvus-lite 3.0

When using the `inline::milvus` provider with `milvus-lite==3.0`, vector queries fail with `KeyError: 'chunk_content'`. The `remote::milvus` provider is not affected as the full Milvus server handles `output_fields=["*"]` correctly.

The `query_vector` method uses `output_fields=["*"]` in `client.search()`. In milvus-lite 3.0 (pure Python rewrite), `["*"]` no longer expands to include JSON fields in search results - it only returns the primary key. The other query methods (`query_keyword`, `query_hybrid`) already use `output_fields=["chunk_content"]` explicitly and are not affected.

**Repro:**
1. Configure OGX with `inline::milvus` provider (uses milvus-lite)
2. Ensure `milvus-lite>=3.0` is installed
3. Create a vector store, insert chunks
4. Query with `mode: "vector"` (or default mode)

**Error:**
```
KeyError: 'chunk_content'
```
at `src/ogx/providers/remote/vector_io/milvus/milvus.py` line 253.

**Impact:** `/v1/vector-io/query` returns 500, `/v1/vector_stores/{id}/search` returns empty results (error caught internally).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `53b473198c36fd06906ea25a212308a98625f31e`.  There
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
{"case_id": "ogx_ai_ogx__6090__53b4731",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
