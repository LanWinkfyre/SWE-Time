# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Web Chat UI silently drops a model's configured system_prompt on a fresh conversation

## Description

A model's configured `system_prompt` (set in the model YAML, `LLMConfig.SystemPrompt`) is silently ignored by the web Chat UI for a fresh conversation, even though it works correctly via direct API calls to the same `/v1/chat/completions` endpoint. This makes the model give confused/context-free answers to the built-in "Explain how this works" / "Help me write code" / etc. suggestion buttons on a brand new chat, since the model has no idea what "this" refers to without the system prompt.

## Setup

v4.9.0. Model config includes:
```yaml
name: qwen3-8b
system_prompt: "You are a helpful AI assistant running locally via LocalAI, a self-hosted, open-source inference platform. Answer questions clearly and directly. If a request is ambiguous or missing needed context, say so and ask for what you need rather than guessing."
...
```

## Reproduction

1. Direct API call, no `system` message in the request:
   ```bash
   curl -X POST /v1/chat/completions -d '{"model":"qwen3-8b","messages":[{"role":"user","content":"Explain how this works"}]}'
   ```
   → Model correctly infers "this" = itself/the chat interface and gives a coherent, on-topic answer. Confirmed via debug logs that the configured `SystemPrompt` is loaded into the effective model config for the request.

2. Same model, same prompt, sent from the Chat page in the web UI (fresh "New Chat", default Chat Settings, "System Prompt" field left at its placeholder / never touched):
   → Model responds asking "Could you please specify what you'd like me to explain?" — i.e., it received *no* context at all. `usage.prompt_tokens` for this request was 13 — far too small to include the ~50-word configured system prompt, confirming it was never part of the request the model saw.

## Suspected root cause

The web UI's Chat Settings panel has a per-conversation "System Prompt" field. It's very likely the frontend always includes a `{"role":"system","content":"<field value>"}` message at `messages[0]` — even when that field is empty/untouched — rather than omitting the system message entirely when the user hasn't set one. Server-side, the chat template only injects the model's configured default when no `system`-role message is already present at `messages[0]`:
```jinja
{%- if messages[0].role == 'system' %}
    {{- messages[0].content + '\n\n' }}
{%- endif %}
```
An explicit-but-empty system message from the UI satisfies this check and suppresses the backend default, whereas a request with no system message at all (like a plain `curl` call) lets the backend's own `system_prompt` apply.

## Expected behavior

A per-model `system_prompt` configured server-side should be the effective default for a fresh chat in the web UI too, the same as it is for a bare API call — at minimum, the Chat Settings "System Prompt" field should be pre-populated with the model's configured value (so the two stay in sync and it's obvious to the user what's actually being sent), or the frontend should omit the `system` message entirely when the field is untouched/empty rather than sending it blank.

## Impact

This directly breaks the built-in suggestion buttons ("Explain how this works", "Help me write code", "Summarize a document", "Brainstorm ideas") on every fresh chat for any model that relies on a configured `system_prompt` for context, since the web UI is the primary way most users will interact with these models.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2bbcfb3ec6975614919da0a8c6b093bdec1bac68`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__11834__2bbcfb3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
