# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
stream_processor: destroyed input instance is used after initialization failure

## Summary

`flb_sp_stream_create()` destroys the private input instance when
`flb_input_instance_init()` returns `-1`, but does not return from the function.
It stores the destroyed pointer in `stream->in` and passes it to later input,
metrics, and storage functions.

## Bug detail

Affected source:

- `src/stream_processor/flb_sp_stream.c:67-148`, stream creation
- `src/stream_processor/flb_sp_stream.c:161-168`, stream destruction

Failure path:

1. The private input is created at line 67.
2. `flb_input_instance_init(in, sp->config)` fails at line 122.
3. Lines 125-126 call `flb_input_instance_exit()` and
   `flb_input_instance_destroy(in)`, so `in` is no longer valid.
4. Line 128 stores the destroyed pointer in `stream->in`.
5. Line 131 passes it to `flb_input_collector_start()`.
6. When metrics are enabled, line 135 reads `in->metrics`.
7. Line 143 passes it to `flb_storage_input_create()`.
8. If storage initialization fails, line 147 calls
   `flb_sp_stream_destroy()`. Lines 165-166 may then exit and destroy the same
   stale pointer again.

## Trigger

The path requires `flb_input_instance_init()` to return `-1`. For the dynamic
`in_stream_processor` input, possible causes include allocation failure in
`cb_sp_init()`, collector setup failure, processor initialization failure, or
other initialization failures. Event-channel failure alone does not exercise
this branch in the current non-threaded path because it is logged and execution
continues.

## Impact / severity

Severity: **Low — potential UAF in an initialization error path**.

If the branch is reached, the process may crash or encounter undefined behavior
through a freed input object; repeated destruction may also corrupt allocator
state. No code execution was demonstrated, and the path is not currently shown
to be reachable from ordinary remote input.

## Proposed fix

After destroying the failed input, release only the stream metadata and return.
Do not call `flb_sp_stream_destroy()` because it assumes ownership of a valid
`stream->in`:

```diff
diff --git a/src/stream_processor/flb_sp_stream.c b/src/stream_processor/flb_sp_stream.c
@@ -122,9 +122,14 @@ int flb_sp_stream_create(struct flb_sp *sp, struct flb_sp_task *task)
     if (ret == -1) {
         flb_error("[sp] cannot initialize instance of in_stream_processor");
         flb_input_instance_exit(in, sp->config);
         flb_input_instance_destroy(in);
+        flb_sds_destroy(stream->name);
+        flb_sds_destroy(stream->tag);
+        flb_free(stream);
+        return -1;
     }
     stream->in = in;
```

A cleanup-label implementation with explicit ownership tracking would also be
appropriate.
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
{"case_id": "fluent_fluent_bit__12204__ae51533",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
