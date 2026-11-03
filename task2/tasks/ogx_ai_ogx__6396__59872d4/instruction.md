# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Docling file processors drop headings and page numbers from chunks

### System Info

OGX main, tested at commit 0443aa634a1f.

Tested with:

- remote::docling-serve in sync mode
- remote::docling-serve in async mode
- inline::docling
- Docling Serve v1.26.0
- PGVector as the vector store

### Information

- [ ] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

The Docling file processors do not preserve all structural metadata produced by Docling.

For remote::docling-serve, Docling Serve returns headings and page_numbers as top-level fields on every chunk. OGX currently looks for headings under a nested meta object. That object is not present
in the real Docling Serve response.

The same problem exists in async mode. The typed Docling response has headings and page_numbers directly on the chunk object, but OGX looks for them under raw_chunk.meta.

The inline Docling processor has a related problem. Native Docling chunks keep headings under doc_chunk.meta.headings. Page numbers can be found in the provenance of the chunk's document items. OGX
does not currently extract both values correctly.

This causes silent metadata loss. The chunk text is stored correctly, but headings and page numbers are missing from the chunk metadata.

This makes it difficult for applications to create precise citations such as:

- document name and section
- document name and page number
- document name, section, and page number

Steps to reproduce with remote::docling-serve:

1. Configure OGX to use remote::docling-serve.
2. Upload a PDF that has headings and more than one page.
3. Process the file using an automatic or static chunking strategy.
4. Inspect the response from Docling Serve. Its chunks contain top-level headings and page_numbers.
5. Inspect the chunks produced by OGX. The headings and page_numbers are missing from their metadata.

The fix should:

- Read headings and page_numbers directly from sync Docling Serve responses.
- Read headings and page_numbers directly from async typed responses.
- Keep support for the older nested meta shape as a fallback.
- Read headings and page numbers from native Docling chunk metadata in inline mode.
- Add tests using the real response shapes.

### Error logs

There is no error or traceback.

The file is processed successfully, but headings and page numbers are silently left out of the chunk metadata.


### Expected behavior

OGX should preserve structural metadata produced by Docling.

For example, a processed chunk should contain metadata like:

```
{
  "filename": "manual.pdf",
  "headings": ["Installation", "Database setup"],
  "page_numbers": [4, 5]
}

```
Empty headings or page numbers can be left out.

The behavior should work for remote Docling Serve in both sync and async mode, and for the inline Docling processor.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `59872d43931e4bd288d0de69e129c6eda9829d7a`.  There
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
{"case_id": "ogx_ai_ogx__6396__59872d4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
