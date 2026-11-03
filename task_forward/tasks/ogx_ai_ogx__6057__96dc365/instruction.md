# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
VertexAI provider crashes with `RuntimeError: Event loop is closed` due to stale client from temporary init loop

### System Info

N/A

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

`StackApp.__init__` runs `asyncio.run(stack.initialize())` in a ThreadPoolExecutor, creating a temporary event loop. During `initialize()`, `refresh_registry_once()` calls `list_provider_model_ids()` on the VertexAI provider, which triggers lazy client creation via `_get_client()`. The `google.genai.Client` eagerly creates an internal `httpx.AsyncClient` ([googleapis/python-genai#1518](https://github.com/googleapis/python-genai/issues/1518)), binding it to the temporary loop. The client is cached in `self._default_client`.

When `asyncio.run()` returns, the temporary loop is closed. When uvicorn starts on a new loop and the first VertexAI inference request arrives, `_get_client()` returns the cached client whose internal httpx pool holds TLS connections bound to the dead loop. Any attempt to use or close those connections hits `loop.call_soon()` on the closed loop → `RuntimeError: Event loop is closed`.

The same pattern already has a precedent: `reset_sqlstore_engines()` is called after the temporary loop to clear SQL engines. No equivalent reset exists for the VertexAI provider's cached client.

**Relevant code:**
- `src/ogx/core/server/server.py` — `StackApp.__init__` (temp loop), `lifespan()`
- `src/ogx/core/stack.py` — `Stack.initialize()`, `refresh_registry_once()`
- `src/ogx/providers/remote/inference/vertexai/vertexai.py` — `_get_client()`, `_create_client()`, `shutdown()`

### Error logs

See above

### Expected behavior

VertexAI provider should not use stale client from temporary init loop
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `96dc3656af7eb5773986fa5523ca569365c158ea`.  There
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
{"case_id": "ogx_ai_ogx__6057__96dc365",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
