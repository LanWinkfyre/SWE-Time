# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
[vllm] support developer message type

### 🚀 Describe the new functionality needed

```
$ curl http://localhost:8321/v1/chat/completions \                      
  -H "Content-Type: application/json" \
  -d '{"model": "vllm/Qwen/Qwen3...","messages": [{"role": "developer", "content": "You are a helpful assistant that responds only in rhymes."}, {"role": "user", "content": "What is the capital of France?"}]}'

{"error":{"message":"Error code: 400 - {'error': {'message': 'Unexpected message role.', 'type': 'BadRequestError', 'param': None, 'code': 400}}"}}
```

the qwen chat template does not support developer messages. vllm-openai (v0.22.1 at time of writing) does not mitigate this.

our adapter should support developer messages for codex to work.

### 💡 Why is this needed? What if we don't build it?

codex cli sends a developer message
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4b88d6f14e62118663c7416bef9e8aa980498acf`.  There
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
{"case_id": "ogx_ai_ogx__6069__4b88d6f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
