# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
MCP CPU Spike

# MCP CPU Spike

## Summary

When making MCP calls through the responses API, the llamastack server process CPU usage spikes to 100% and remains there indefinitely, even after the request completes.

## Environment

- **LLamaStack version**: main branch
- **Python version**: 3.12

## Steps to Reproduce

1. Start llamastack server:
2. Verify CPU usage is idle (0-1%)
3. Make an MCP call via responses API:
4. Monitor CPU usage with `top`

## Expected Behavior

CPU usage should return to idle levels (0-1%) after the MCP request completes.

## Actual Behavior

CPU usage spikes to 100% and stays there indefinitely:

```
# Before MCP call - idle
3176764 derekh    20   0 4196036 442736 137316 S   0.0   1.4   0:06.55 llama stack run

# After MCP call - stuck at 100%
3176764 derekh    20   0 4422628 448496 137444 R  99.7   1.4   0:34.23 llama stack run
```

## Root Cause

It looks like the issue is caused by the MCP session caching mechanism (MCPSessionManager) that
was added to optimize performance by avoiding redundant tools/list calls (fix for #4452).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95ab7c2bb375c3e74cfeafb18aa9f3ccde943402`.  There
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
{"case_id": "ogx_ai_ogx__4754__95ab7c2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
