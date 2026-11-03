# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
wire docling and unstructured into auto file processor

### 🤔 What is the technical debt you think should be addressed?

The inline::auto file processor only imports and dispatches to pypdf and markitdown. Docling and unstructured exist as standalone providers (inline::docling, remote::docling-serve, remote::unstructured-api) but are not wired into auto. Users of the default starter distribution get no docling or unstructured support unless they explicitly configure a provider.

This means auto's format coverage has gaps. docling and unstructured handle formats (e.g. complex PDFs with tables, scanned documents) that pypdf and markitdown handle poorly or not at all, but auto can't route to them.

### 💡 What is the benefit of addressing this technical debt?

  - Users get better document processing out of the box without manual provider configuration.
  - Enables a single inline::auto entry point that can route to the best provider for a given file type, including docling and unstructured for formats where they excel.
  - Requires designing a proper fallback/priority mechanism across providers, which will make auto extensible for future providers as well.

Design considerations for the implementation:
  - inline::docling runs in-process and can consume 20GB+ RAM / saturate CPUs. Auto dispatch should account for whether to route to inline vs remote, or whether process isolation is available.
  - The docling-serve async API (/v1/convert/file/async → poll → result) is the recommended pattern from docling maintainers. Auto dispatch should be compatible with async-capable providers.
  - remote::unstructured-api (#6076) is remote-only, so the fallback logic needs to handle providers that may or may not be configured/reachable.
  
  Context: #6076, #6095, #6100, opendatahub-io/ogx-distribution#388, RHOAIENG-69345

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0a1c29e509b11a74dc969687f9d4b224c1b66f8b`.  There
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
{"case_id": "ogx_ai_ogx__6130__0a1c29e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
