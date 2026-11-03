# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
[Docs] Quick start guide with Ollama does not boot useable server

### System Info

N/A

### Information

- [x] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The new quick start guide provides the following instructions to start a server
```
ollama pull llama3.2:3b
uv init my-ai-app && cd my-ai-app
uv add 'llama-stack[starter]' openai
uv run llama stack run starter
```
Following these instructions yields a result where only embedding models are shown
```
curl http://localhost:8321/v1/models | jq
{
  "object": "list",
  "data": [
    {
      "id": "sentence-transformers/nomic-ai/nomic-embed-text-v1.5",
      "object": "model",
      "created": 1776135231,
      "owned_by": "llama_stack",
      "custom_metadata": {
        "model_type": "embedding",
        "provider_id": "sentence-transformers",
        "provider_resource_id": "nomic-ai/nomic-embed-text-v1.5",
        "embedding_dimension": 768
      }
    },
    {
      "id": "transformers/Qwen/Qwen3-Reranker-0.6B",
      "object": "model",
      "created": 1776135231,
      "owned_by": "llama_stack",
      "custom_metadata": {
        "model_type": "rerank",
        "provider_id": "transformers",
        "provider_resource_id": "Qwen/Qwen3-Reranker-0.6B"
      }
    }
  ]
}
```
I made two attempts to fix base on the current docs:
1. did a `ollama run llama3.2:3b --keepalive 60m` to ensure a model was running
2. prefixed command with `OLLAMA_URL=http://localhost:11434 uv run llama stack run starter` to ensure Ollama inference provider was enabled

however this did not fix the issue, though it did produce the error below

i confirmed as well that the ollama server shows models as expected
```
curl http://localhost:11434/v1/models | jq
{
  "object": "list",
  "data": [
    {
      "id": "llama3.2:3b",
      "object": "model",
      "created": 1776114016,
      "owned_by": "library"
    },
    {
      "id": "qwen2.5-coder:32b",
      "object": "model",
      "created": 1744853552,
      "owned_by": "library"
    },
    {
      "id": "qwen2.5-coder:14b",
      "object": "model",
      "created": 1744853325,
      "owned_by": "library"
    },
    {
      "id": "qwen2.5-coder:7b",
      "object": "model",
      "created": 1744655225,
      "owned_by": "library"
    },
    {
      "id": "all-minilm:latest",
      "object": "model",
      "created": 1744399739,
      "owned_by": "library"
    },
    {
      "id": "granite3.2:latest",
      "object": "model",
      "created": 1744039862,
      "owned_by": "library"
    },
    {
      "id": "llama3.2:latest",
      "object": "model",
      "created": 1743775396,
      "owned_by": "library"
    }
  ]
}
```

### Error logs

```
ERROR    2026-04-14T02:53:44.555541Z  llama_stack.providers.utils.inference.openai_mixin:530 list_provider_model_ids()  
         failed   category=providers::utils error=404 page not found provider=OllamaInferenceAdapter 
```

### Expected behavior

Server starts and shows Ollama models as expected
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3949f9f5b18d144ed0b0bedfcecd90679ab020eb`.  There
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
{"case_id": "ogx_ai_ogx__5551__3949f9f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
