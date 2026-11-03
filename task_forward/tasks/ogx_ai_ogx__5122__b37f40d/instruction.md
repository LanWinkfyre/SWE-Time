# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Gemini OpenAI API overcounts tokens in streaming mode

### System Info

Using Gemini Inference Provider

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

Bug is described here: https://discuss.ai.google.dev/t/endpoint-https-generativelanguage-googleapis-com-v1beta-openai-chat-completions-is-not-compliant-with-api-specs/127400

Workarounds suggested:

- For Custom Implementations: Modify your stream-processing loop to not accumulate the usage field. Instead, only capture the usage data from the very last chunk (or the one where finish_reason is not null).

- For Effect-TS Users: This specific bug was fixed in version 3.14.1 of @effect/ai-openai. You should update to the latest version to handle "arbitrary length StreamChunkParts."

- For OpenAI SDK Users: Some developers have found that setting stream_options: { include_usage: false } and instead using a separate token_count metadata call is safer until Google aligns its endpoint with the spec.


### Error logs

n/a

### Expected behavior

Only return usage tokens in the last chunk. dont overcount from each chunk or return usage in each chunk
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b37f40d1f692f255810fac04cb2d63fcc71fff6d`.  There
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
{"case_id": "ogx_ai_ogx__5122__b37f40d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
