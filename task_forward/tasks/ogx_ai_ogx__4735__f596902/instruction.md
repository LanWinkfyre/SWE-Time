# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Responses API reasoning summaries from providers that do NOT provide them

### 🚀 Describe the new functionality needed

OpenAI's Responses API lets you request reasoning summaries (e.g., `"reasoning": {"summary": "concise"}`) but Llama Stack does not implement this functionality. Issue #4697 proposes to pass through these parameter settings to those inference providers that support them.  This issue is intended to address providers that do not provide reasoning summaries but DO provide full reasoning content.  For example, both Ollama and vLLM appear to provide reasoning text through their chat completions API when used with reasoning models such as GPT-OSS and Qwen.

### 💡 Why is this needed? What if we don't build it?

It is missing for compatibility. Also, the content is useful for explaining and debugging complex workflows.

### Other thoughts


For this situation, Llama Stack will need to get the reasoning content from the original chat completion request and then make a second call back to the inference server to ask it to summarize that reasoning content.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f596902bf92634334cd9c75cf3986c2f78c8c6ee`.  There
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
{"case_id": "ogx_ai_ogx__4735__f596902",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
