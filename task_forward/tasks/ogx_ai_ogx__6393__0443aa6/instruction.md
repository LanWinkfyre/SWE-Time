# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
remote::docling-serve can send an empty file when using async mode

### System Info

OS: Red Hat Enterprise Linux 10.1, x86_64
Podman: 5.6.0
Python: 3.12.13
OGX: 1.3.1.dev0

The affected code is also present in OGX 1.3.0.

docling-slim: 2.119.0
docling-serve: v1.26.0 CPU container
Provider: remote::docling-serve
Provider mode: async (the default)

No GPU is required to reproduce the problem.

### Information

- [ ] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

When `remote::docling-serve` uses async mode, OGX writes the uploaded
document to a `NamedTemporaryFile` and immediately gives the temporary
file path to `AsyncDoclingServiceClient`.

The temporary file is not flushed first. The Docling client opens the
same path using another file handle, so it can read an empty file.

This happens in both async methods:

```
- `_convert_no_chunk_async()`
- `_convert_and_chunk_async()`
```

It affects conversion with and without chunking. It is easiest to
reproduce with a small file because the full write remains in Python's
buffer.

The temporary file also has no original extension. Docling Serve
therefore receives a temporary filename and
`application/octet-stream` instead of the original filename and MIME
type.

This code van have been introduced as part of
https://github.com/ogx-ai/ogx/pull/6014.

## Steps to reproduce

Configure the Docling Serve provider in async mode:

```yaml
file_processors:
  - provider_id: docling-serve
    provider_type: remote::docling-serve
    config:
      base_url: http://localhost:5001
      mode: async
```
Start OGX and Docling Serve.

Create a small HTML document:

```
printf '<html><body><p>Hello from a small document.</p></body></html>' \
  > /tmp/small.html
```

Send it to the file processor with chunking enabled:

```
curl -sS \
  -F 'file=@/tmp/small.html;type=text/html' \
  -F 'chunking_strategy={"type":"auto"}' \
  http://localhost:8321/v1alpha/file-processors/process
```

The response contains no chunks.

The same problem can be reproduced by uploading a small document
through /v1/files and then adding it to a vector store. In that flow,
file ingestion fails with:

No chunks were generated from the file

The buffering problem can also be demonstrated without Docling:

```
import tempfile
from pathlib import Path

content = b"x" * 2414

with tempfile.NamedTemporaryFile() as tmp:
    tmp.write(content)

    print(len(Path(tmp.name).read_bytes()))
    # Prints 0

    tmp.flush()

    print(len(Path(tmp.name).read_bytes()))
    # Prints 2414
```

## Suggested fix

Instead of creating a temporary file, pass a Docling DocumentStream
containing the original filename and bytes:

```
from io import BytesIO
from docling_core.types.io import DocumentStream

source = DocumentStream(
    name=filename,
    stream=BytesIO(content),
)
```

Use this source in both `client.submit()` and
`client.submit_chunk()`.

This preserves:

- The complete document content
- The original filename
- The file extension
- The correct MIME type

A smaller fix would call tmp.flush() and create the temporary file
with the correct suffix. However, DocumentStream avoids the temporary
file and preserves the full original filename.

Tests should cover both async conversion paths and assert that the
client receives the original filename and all input bytes. An
integration test should use a small document so the buffering problem
is reliably detected.

### Error logs

Docling Serve receives an empty file:

```
File 0: name=tmppbuw_vps, size=0 bytes,
md5=d41d8cd98f00, content_type=application/octet-stream
```

Input document tmppbuw_vps with format None does not match any allowed format.

Document tmppbuw_vps failed to convert.

Processed 1 docs generating 0 chunks.

When the document is added to a vector store, OGX reports:

File ingestion ended with status 'failed':
```
{
  "code": "server_error",
  "message": "No chunks were generated from the file"
}
```

There is no OGX Python traceback because the Docling async request itself succeeds. It returns a result containing no chunks.

### Expected behavior

Docling Serve should receive the complete uploaded document with its
original filename and correct MIME type.

Async conversion should produce the same document or chunks as sync
conversion. Adding the file to a vector store should complete
successfully.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0443aa634a1fa0f1e7fb2070874988653e245e39`.  There
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
{"case_id": "ogx_ai_ogx__6393__0443aa6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
