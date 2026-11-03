# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug: runtime download of tiktoken cl100k_base encoding breaks air-gapped deployments

### System Info

I've found this problem when running 0.6.0.1+rhai0 in a disconnected OpenShift cluster running the Red Hat Llama Stack Distribution included in OpenShift AI 3.4 EA2 (nightly build). 

The disconnected cluster had an https_proxy configured in order to call external LLMs. In the proxy logs I could see how https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken was being downloaded. 
If the cluster was 100% disconnected and the models were deployed locally, vector stores wouldn't not work because of this.

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

## Description

Since PR #4870 (merged Feb 9, 2026), the first vector store file attachment triggers a runtime
HTTP download of the tiktoken `cl100k_base` encoding file (~1.7 MB) from
`https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken`.

This breaks air-gapped and network-restricted deployments where outbound internet access is
unavailable or limited to approved endpoints. The server fails on the first
`vector_stores.files.create()` call because it cannot reach Azure Blob Storage.

## Root Cause

PR #4870 replaced the local Llama 3 tokenizer with `tiktoken.get_encoding("cl100k_base")` for
document chunking. Unlike the previous tokenizer — which loaded BPE ranks from a local `.model`
file via `tiktoken.load_tiktoken_bpe()` — the new code path requires a network fetch on first use:

```python
# src/llama_stack/providers/utils/memory/vector_store.py

@cache
def _get_encoding(name: str) -> tiktoken.Encoding:
    return tiktoken.get_encoding(name)  # downloads from openaipublic.blob.core.windows.net

def make_overlapped_chunks(..., chunk_tokenizer_encoding: str = "cl100k_base"):
    encoding = _get_encoding(encoding_name)
    tokens = encoding.encode(text)
    ...
```

The previous code used `Tokenizer.get_instance()` from
`llama_stack.models.llama.llama3.tokenizer`, which required no network access at all.

## Impact

- Air-gapped and network-restricted deployments (common in enterprise OpenShift / Kubernetes
  environments) cannot use vector store file operations without granting egress to
  `openaipublic.blob.core.windows.net`.
- The failure only manifests at runtime on the first file attachment, making it difficult to
  catch during deployment validation.
- This is the same class of issue as [BerriAI/litellm#23218](https://github.com/BerriAI/litellm/issues/23218).

## Suggested Fix

### Option A — Pre-cache at image build time (immediate, no code change)

Add two lines to [`containers/Containerfile`](https://github.com/llamastack/llama-stack/blob/main/containers/Containerfile),
after the cleanup step and before the entrypoint setup:

```dockerfile
# Pre-cache tiktoken cl100k_base encoding to avoid runtime download
# from openaipublic.blob.core.windows.net (used by vector_store chunking)
ENV TIKTOKEN_CACHE_DIR="/.cache/tiktoken"
RUN python3 -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"
```

This should also be:
1. **Added to the [Building Custom Distributions](https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html) documentation**
   as a recommended step for custom Containerfiles, so downstream image builders are aware of
   the runtime network dependency.
2. **Mentioned in the Containerfile comments** explaining why the pre-caching is needed.

### Option B — Bundle the encoding in the package

Ship the `cl100k_base.tiktoken` file alongside the llama-stack source and point
`TIKTOKEN_CACHE_DIR` at it, removing the network dependency from both image builds and runtime.

### Option C — Revert to a local tokenizer

Revert to a tokenizer that loads from local files (e.g. the Llama 3 tokenizer used before #4870),
or make the tokenizer fully configurable so deployments can choose a local-only option.

## Environment

- Llama Stack version: any version including PR #4870 (post Feb 9, 2026)
- Deployment: air-gapped / restricted-egress Kubernetes / OpenShift
- Triggered by: `vector_stores.files.create()` → `make_overlapped_chunks()` → `tiktoken.get_encoding("cl100k_base")`

## References

- Introducing PR: #4870
- tiktoken added as dep: #1483
- Upstream Containerfile: https://github.com/llamastack/llama-stack/blob/main/containers/Containerfile
- Building Custom Distributions docs: https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html
- Similar issue in litellm: https://github.com/BerriAI/litellm/issues/23218
- tiktoken offline FR: https://github.com/openai/tiktoken/issues/317


### Expected behavior

vector stores in llama-stack should work on disconnected environments
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0c152c3bdcedf028df201c0a16ee65467ba5c29e`.  There
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
{"case_id": "ogx_ai_ogx__5337__0c152c3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
