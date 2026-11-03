# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
MarkItDown file processor vulnerable to ZIP bomb resource exhaustion

MarkItDown processes ZIP-based Office formats (DOCX, PPTX, XLSX) without
validating decompressed size or entry count. A malicious archive can cause
unbounded memory usage and CPU consumption on the server.

Observed with a 1GB decompressed zip: 17GB RAM, 100% CPU, request never
completes (or takes longer than I was prepared to wait, while leaving CPU at 100%).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a0bd9f55971a2897d3bac4fef0b0a01a03aafcfa`.  There
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
{"case_id": "ogx_ai_ogx__6099__a0bd9f5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
