# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Bug: usage_bytes always 0 - RAG file_search pipeline not indexing files (FAISS + Ollama)

### System Info

**OGX version:** 1.4.0
**Python version:** 3.14
**OS:** RHEL (Linux)
**Inference provider:** Ollama
**Vector store provider:** FAISS (default)

### Information

- [x] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

When uploading a file and creating a vector store using the OpenAI-compatible API, the file shows `status: processed` and `file_counts.completed: 1`, but `usage_bytes` remains `0` indefinitely. The model never receives retrieved context, making `file_search` completely non-functional.

### Steps to reproduce

```python
import httpx
import time
from openai import OpenAI

client = OpenAI(
    base_url="https://localhost:8321/v1",
    api_key="fake",
    http_client=httpx.Client(verify=False)
)

file = client.files.create(
    file=open("document.pdf", "rb"),
    purpose="assistants",
)
print("FILE:", file.id)

vector_store = client.vector_stores.create(
    name="my-docs",
    file_ids=[file.id],
)
print("VECTOR STORE:", vector_store.id)

for _ in range(15):
    files = client.vector_stores.files.list(vector_store.id)
    for item in files:
        print(f"STATUS: {item.status} | USAGE: {item.usage_bytes}")
    time.sleep(2)

response = client.responses.create(
    model="ollama/qwen2.5:1.5b",
    input="Summarize the key points of the document",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store.id],
    }],
)
print(response.output_text)
```
### Actual behavior

```
FILE: file-449601f88e884badb6cc93a5cb5a4766
VECTOR STORE: vs_ae89a901-0faf-469f-82ad-4d815985fe9b
STATUS: completed | USAGE: 0
STATUS: completed | USAGE: 0
STATUS: completed | USAGE: 0
... (repeats indefinitely)
```

The model responds as if no document was provided, ignoring the vector store entirely.

### Vector store metadata (from GET /v1/vector_stores)

```json
{
  "usage_bytes": 0,
  "file_counts": { "completed": 1, "total": 1 },
  "status": "completed",
  "metadata": {
    "provider_id": "faiss",
    "embedding_model": "ollama/nomic-embed-text",
    "embedding_dimension": "768"
  }
}
```

### Notes

- The embedding model `ollama/nomic-embed-text:latest` is available and registered.
- Both `.txt` and `.pdf` files reproduce the issue.
- The chunking/embedding step appears to be silently skipped, no error is returned.
- Workaround: manually extract text with `pypdf` and pass it directly in the prompt.

### Error logs

No error is raised. The pipeline silently completes with usage_bytes: 0.
Server logs show no exception or warning related to chunking or embedding.
The file processor reports status: "processed" but no vectors are written to FAISS.

### Expected behavior

`usage_bytes` should reflect the indexed content size, and the model should receive retrieved chunks as context.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d8a75bb7d4f70477b3f25c4e5942771f98caf07e`.  There
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
{"case_id": "ogx_ai_ogx__6542__d8a75bb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
