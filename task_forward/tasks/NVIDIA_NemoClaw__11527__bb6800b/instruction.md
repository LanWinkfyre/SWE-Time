# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
llama-cpp-local discards meta.n_ctx, NEMOCLAW_CONTEXT_WINDOW defaults to 128k ignoring --ctx-size

### Investigation Summary

probeLlamaCppAttachment() already reads meta.n_ctx from /v1/models during fingerprinting but returns only { ok: true, model }, discarding the value. [resolveContextWindowForModel()](resolveContextWindowForModel) has no llama-cpp-local branch, so it falls through to defaultCloudContextWindow() and bakes 128k into the sandbox regardless of the actual --ctx-size passed to llama-server.

### Description

When using NemoClaw with a llama-server (llama.cpp) backend, NEMOCLAW_CONTEXT_WINDOW is never auto-detected and silently falls back to the default, even when the server is launched with an explicit --ctx-size.

### Reproduction Steps

llama-server -m Qwen3.5-35B-A3B-Q4_K_M.gguf --ctx-size 65536
GET /v1/models returns:
json
"meta": { "n_ctx": 65536, "n_ctx_train": 262144, ... }

NemoClaw finds no max_model_len, returns null, and bakes the default 131072 into the sandbox config.

**Expected**: NemoClaw detects 65536 from meta.n_ctx.
**Actual**: NemoClaw ignores meta.n_ctx, logs nothing, uses default.

### Environment

NemoClaw latest from main branch

### Debug Output

NA

### Logs

```shell

```

### Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bb6800b8fbb15b962822a1ef92a460dd1eab0229`.  There
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
{"case_id": "NVIDIA_NemoClaw__11527__bb6800b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
