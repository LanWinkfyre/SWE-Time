# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Add support for IVFFlat (Inverted File with Flat Compression) vector index for ANN search in PGVector

### 🚀 Describe the new functionality needed

Currently in Llama Stack there is support only for HNSW vector index for ANN search in PGVector provider:

```
@json_schema_type
class PGVectorVectorIOConfig(BaseModel):
    host: str | None = Field(default="localhost")
    port: int | None = Field(default=5432)
    db: str | None = Field(default="postgres")
    user: str | None = Field(default="postgres")
    password: str | None = Field(default="mysecretpassword")
    distance_metric: Literal["COSINE", "L2", "L1", "INNER_PRODUCT"] | None = Field(
        default="COSINE", description="PGVector distance metric used for vector search in PGVectorIndex"
    )
    hnsw_m: int | None = Field(
        gt=0,
        default=16,
        description="PGVector's HNSW index parameter - maximum number of edges each vertex has to its neighboring vertices in the graph",
    )
    hnsw_ef_construction: int | None = Field(
        gt=0,
        default=64,
        description="PGVector's HNSW index parameter - size of the dynamic candidate list used for graph construction",
    )
    persistence: KVStoreReference | None = Field(
        description="Config for KV store backend (SQLite only for now)", default=None
    )
```

My proposal is to extend `PGVectorVectorIOConfig` allowing users to choose between HNSW and IVFFlat indexes for ANN search in pgvector along with configuring each index's' specific parameters. Both indexes are vitally important for performance optimization of vector search and have own pros and cons. Users which prioritize faster index build times and less memory consumption would benefit from choosing [IVFFlat](https://github.com/pgvector/pgvector?tab=readme-ov-file#ivfflat) as main vector index. Therefore, this needs to be implemented.

### 💡 Why is this needed? What if we don't build it?

### This feature will have the following impact:
1. Enables flexibility of vector index choices in pgvector for users depending on their priorities, goals and use cases. 
2. Enhances pgvector UX in Llama Stack.

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c82c398330eea8084bf74b361761a5e4b4241739`.  There
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
{"case_id": "ogx_ai_ogx__4745__c82c398",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
