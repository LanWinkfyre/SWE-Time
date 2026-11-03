# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Inline file processors block the event loop during parsing

Inline file processors (pypdf, markitdown, docling) run CPU-intensive parsing synchronously in the async event loop. A large or complex file blocks the entire server until parsing completes - other requests (including simple /v1/models) stall.

Tested with a ~4.5MB text file: concurrent /v1/models requests spiked to 6500ms+ latency during processing, vs the normal ~5ms.

The remote docling-serve provider avoids this because parsing happens over HTTP, but all inline processors are affected.

**Fix:** Wrap synchronous parsing calls in `asyncio.to_thread()` to offload them to the thread pool.

**Affected files:**
- `src/ogx/providers/inline/file_processor/pypdf/pypdf.py`
- `src/ogx/providers/inline/file_processor/markitdown/markitdown_processor.py`
- `src/ogx/providers/inline/file_processor/docling/docling.py`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `16c0ad8ee0d780f890b385f8280078b6e9fb0234`.  There
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
{"case_id": "ogx_ai_ogx__6094__16c0ad8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
