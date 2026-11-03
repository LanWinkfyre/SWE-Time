# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out_s3: current_buffer_size underflows at startup when store_dir has leftover files — output permanently rejects data ('Buffer is full')

### Bug Report

**Describe the bug**

`out_s3`'s `current_buffer_size` accounting underflows (size_t wrap to ~2^64) whenever Fluent Bit starts with leftover files in `store_dir`. After the wrap, every subsequent buffer write fails the `store_dir_limit_size` check and the output rejects all new data ("Buffer is full") until the process is restarted — and the wrap re-occurs on any restart that again finds leftover files.

**Root cause (verified in v5.0.9 and present on master)**

`set_files_context()` in `plugins/out_s3/s3_store.c` assigns each pre-existing file a real size but never credits it to the running total:

```c
file_size = cio_chunk_get_real_size(fsf->chunk);
if (file_size > 0) {
    s3_file->size = (size_t) file_size;
}
/* ctx->current_buffer_size is NOT incremented here */
```

`ctx->current_buffer_size` starts at 0. When the startup resend (`put_all_chunks()`) successfully uploads a leftover file, `s3_store_file_delete()` runs:

```c
ctx->current_buffer_size -= s3_file->size;   /* 0 - size -> wraps */
```

`current_buffer_size` is `size_t`, so it wraps to `2^64 - <leftover bytes>`. From then on `s3_store_buffer_put()`'s guard

```c
if (ctx->store_dir_limit_size > 0 && ctx->current_buffer_size + bytes >= ctx->store_dir_limit_size)
```

is permanently true and the output logs, per attempted write:

```
[error] [output:s3:s3.3] Buffer is full: current_buffer_size=18446744073709481984, new_data=13772, store_dir_limit_size=2000000000 bytes
```

(`18446744073709481984` = 2^64 − 69632 — exactly the leftover bytes resent and deleted at startup.)

For comparison, v2.2.2's `set_files_context()` left `s3_file->size` at 0 for loaded files, so the delete subtracted 0 — the accounting ignored leftovers but never underflowed. The regression is the size assignment being added without the matching credit.

**To Reproduce**

1. Configure an `s3` output with `store_dir` and a nonzero `store_dir_limit_size`, against any reachable S3 endpoint.
2. Run Fluent Bit with steady input; stop it while at least one buffered file remains in `store_dir` (e.g. kill between `upload_timeout` cycles).
3. Start Fluent Bit again. The startup scan re-sends and deletes the leftover file(s).
4. Every subsequent write to that output fails with `Buffer is full: current_buffer_size=18446744073709...`.

Observed live on two independent instances (arm64, Debian trixie image `ghcr.io/fluent/fluent-bit:5.0.9-debug`), deterministic on every restart-with-leftovers.

**Expected behavior**

Leftover files loaded at startup should be counted into `current_buffer_size` (they occupy the store_dir the limit governs), i.e. `set_files_context()` should also do:

```c
ctx->current_buffer_size += s3_file->size;
```

which both fixes the underflow and makes the limit honest about pre-existing usage. (Defensive clamping in `s3_store_file_delete()` — as `s3_chunk_retry_exhausted_cleanup()` already does — would additionally protect against any other asymmetry.)

**Your Environment**

- Version used: v5.0.9 (also inspected on current master — same code)
- Configuration: `s3` output, `use_put_object on`, `compression gzip`, `total_file_size 8M`, `upload_timeout 10s`, `store_dir` on a persistent volume, `store_dir_limit_size 2G`, `workers 2`
- Environment: Docker (`ghcr.io/fluent/fluent-bit:5.0.9-debug`), linux/arm64 and linux/amd64
- Filters and plugins: custom input plugins (not involved — the accounting is output-side)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ae51533a2d7a1cb8cb817ded61e28e2c6e88be9a`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__12164__ae51533",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
