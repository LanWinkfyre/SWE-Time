# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Serialize tables inside Docling chunks as Markdown

Docling currently serializes tables inside OGX chunks as row triplets. This loses the table layout and makes the retrieved text harder for people and models to understand.

I would like OGX to add an optional `chunking_use_markdown_tables` setting to the `remote::docling-serve` file processor.

When the setting is `true`, tables inside chunks should use normal Markdown table syntax. When it is missing or `false`, the current row-triplet format should stay the same.

This would preserve table headers and rows in the retrieved text. It should make table content easier to use for RAG and more useful when creating precise citations.

The implementation can use Docling's normal convert endpoint with chunk output and custom hybrid chunking options. It supports both the sync and async OGX paths. Tests cover both paths, and the async path was also tested end to end with Docling Serve v1.30.0 and pgvector.

This requires a Docling client and Docling Serve version that support chunk output through the convert endpoint. The client needs `docling-slim` 2.117.0 or newer. Docling Serve v1.30.0 is the version tested so far.

One design question is how OGX should handle older Docling Serve versions. My suggestion is to document the compatible version and return a clear error. Falling back to the old chunking endpoint does not seem useful because the Docling maintainers have said that it is about to be deprecated:
https://github.com/docling-project/docling/pull/3983

I have an implementation here:
https://github.com/pgustafs/ogx/tree/feat/docling-markdown-table-chunks
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `35db76fe8d1110122d1f38e054faa4506ba0b1f4`.  There
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
{"case_id": "ogx_ai_ogx__6403__35db76f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
