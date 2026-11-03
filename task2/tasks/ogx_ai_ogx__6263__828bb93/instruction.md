# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Tool outputs (websearch, file_search) fed unsanitized into LLM context — indirect prompt injection

## Summary

Tool invocation results from `web_search` (Tavily, Brave, Bing) and `file_search` (RAG) providers are passed directly into the LLM context as tool messages with no sanitization, escaping, or trust delimiter. This creates an indirect prompt injection surface: attacker-controlled content in web pages or uploaded documents can hijack the agent's behavior.

## Reproduction

1. Start an OGX server (v1.1.3) with an inference provider, pgvector, and an embedding model
2. Upload a text file via `POST /v1/files` containing hidden prompt injection instructions interleaved with legitimate content
3. Create a vector store, attach the file, wait for indexing
4. Send a benign query via `POST /v1/responses` with `file_search` tool and the vector store
5. The model follows the injected instructions from the document content instead of answering the user's question

Tested against OGX v1.1.3 with `gpt-4o-mini` as the inference backend. The injection payload was followed verbatim — the model output a canary marker, refused to disclose the document's actual data, and repeated fabricated claims planted in the payload.

The same class of attack applies to the websearch providers: an attacker who controls a web page returned by Tavily/Brave/Bing can embed instructions that steer subsequent agent turns.

## Affected code path

1. **Tool providers** return raw content without sanitization:
   - `src/ogx/providers/remote/tool_runtime/tavily_search/tavily_search.py` — `_clean_tavily_response()` returns full Tavily results including page content, serialized via `json.dumps()`
   - `src/ogx/providers/remote/tool_runtime/brave_search/brave_search.py` — same pattern
   - `src/ogx/providers/inline/tool_runtime/file_search/file_search.py` — RAG chunks inserted via `.format()` into `TextContentItem` with no transformation

2. **Agent loop** passes tool results directly to the model:
   - `src/ogx/providers/inline/responses/builtin/responses/tool_executor.py` — `_build_result_messages()` converts `ToolInvocationResult.content` directly to `OpenAIToolMessageParam`
   - `src/ogx/providers/inline/responses/builtin/responses/streaming.py` — tool messages appended to `next_turn_messages` and fed into the next inference call

There is no sanitization, escaping, content filtering, or trust boundary annotation at any layer between tool output and model input.

## Impact

A user asking the agent to "search for X" or "summarize this document" can have the agent's response and subsequent tool calls redirected by content the user never saw. This is particularly impactful when:
- The `/v1/files` endpoint is unauthenticated (allowing arbitrary document upload)
- Multiple tool types are registered (e.g., MCP tools that an injected prompt could invoke)
- No safety API / shield is configured in the deployment

## Suggested mitigations

- Add content sanitization or trust delimiters for tool output before it enters the model context
- Ship `builtin::websearch` disabled by default — gate on API key presence rather than registering the tool group unconditionally
- Document that RAG sources and web search results are untrusted input
- Implement `tool_output` touchpoint shields (as discussed in #3325, closed without implementation)

## References

- OWASP LLM Top 10: LLM01 (Prompt Injection), LLM08 (Excessive Agency)
- CWE-77, CWE-74
- CVSS v3.1: 5.4 (AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N)
- Prior discussion: #3325 (Add safety extensions to the Responses API — closed stale, proposed `tool_output` touchpoint but never implemented)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `828bb932d81b7eae9d477b0fea65de2bda46907d`.  There
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
{"case_id": "ogx_ai_ogx__6263__828bb93",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
