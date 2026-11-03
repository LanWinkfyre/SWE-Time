# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
pypdf file processor rejects owner-encrypted PDFs that pypdf can parse

### System Info

- ogx latest (main branch)
- Python 3.12+
- pypdf 6.10+

### Information

- [x] My own modified scripts

### 🐛 Describe the bug

The `inline::pypdf` file processor in `src/ogx/providers/inline/file_processor/pypdf/pypdf.py` rejects all PDFs where `PdfReader.is_encrypted` returns `True`, including **owner-encrypted PDFs** that require no password to read.

Many corporate and financial documents (e.g., SEC filings, earnings press releases) use PDF owner-encryption to restrict printing/copying, but the content is freely readable without any password. `pypdf` handles these files correctly — `PdfReader` can extract text from them without calling `decrypt()`.

The current check at line 101:

```python
if reader.is_encrypted:
    raise HTTPException(status_code=422, detail="Password-protected PDFs are not supported")
```

This is too broad. `is_encrypted` returns `True` for **any** PDF with encryption metadata, not just password-protected ones. This blocks a common class of publicly available documents from being ingested into vector stores.

### Reproduction

1. Download any corporate PDF with owner-encryption (e.g., IBM quarterly earnings press release from https://www.ibm.com/investor)
2. Upload it to a vector store via the files API
3. The server rejects it with `422: Password-protected PDFs are not supported`
4. But running `PdfReader(file).pages[0].extract_text()` in Python works fine — the content is readable

### Expected behavior

The file processor should attempt to read the PDF before rejecting it. Owner-encrypted PDFs (no password needed) should be processed normally. Only PDFs that actually require a password to read should be rejected.

### Suggested fix

Replace the blanket rejection with an attempt to read:

```python
if reader.is_encrypted:
    try:
        reader.decrypt("")  # empty password works for owner-encrypted PDFs
    except Exception:
        raise HTTPException(status_code=422, detail="Password-protected PDFs are not supported")
```

This preserves the rejection for truly password-protected PDFs while allowing owner-encrypted documents through.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `63b14e03e59f1efeb1a1e3db94beac7ab27f067e`.  There
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
{"case_id": "ogx_ai_ogx__6181__63b14e0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
