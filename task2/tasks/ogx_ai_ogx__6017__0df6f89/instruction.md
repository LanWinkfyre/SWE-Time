# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Empty function tool parameters cause 500 error with Anthropic provider

## Empty function tool parameters cause 500 error with Anthropic provider

**Type:** Bug

### Description

When a function tool is defined with empty parameters (`"parameters": {}`), the Responses API forwards it as-is to the inference provider. Anthropic's OpenAI-compatible endpoint rejects this because `parameters.type` is a required field, returning:

```
500 - tools.0.function.parameters.type: Field required
```

Similarly, if `parameters` contains properties but no `type` field, the request is also rejected.

### Steps to Reproduce

1. Configure OGX with `remote::anthropic` provider
2. Create a response with a no-argument function tool:
```python
client.responses.create(
    model="anthropic/claude-sonnet-4-6",
    input=[{"role": "user", "content": "what's the current time?"}],
    tools=[{
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {},
    }],
)
```
3. Server returns 500

### Verified Against Anthropic API

| `input_schema` | Result | Error |
|---|---|---|
| `{}` | 400 | `tools.0.custom.input_schema.type: Field required` |
| `{"properties": {"tz": {"type": "string"}}}` | 400 | `tools.0.custom.input_schema.type: Field required` |
| `{"type": "object"}` | 200 | Works |
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0df6f8980e44f80ec9eb8726c3108d3eeb60bea6`.  There
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
{"case_id": "ogx_ai_ogx__6017__0df6f89",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
