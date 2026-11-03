# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out_azure_blob: partial allocation failure leaves dangling SDS outputs

## Summary

`azb_db_file_oldest_ready()` stores allocated SDS objects directly in output
parameters. If a later SDS allocation fails, it destroys earlier objects but
does not clear the output pointers. The caller subsequently destroys those
non-`NULL` dangling pointers again.

## Bug detail

Affected source:

- `plugins/out_azure_blob/azure_blob_db.c:979-1067`,
  `azb_db_file_oldest_ready()`
- `plugins/out_azure_blob/azure_blob.c:1551-1750`, caller and cleanup

Failure paths:

1. `*path` is assigned at line 996.
2. If `*part_ids` allocation fails at line 1006, line 1008 destroys `*path`
   but does not set `*path = NULL`.
3. If `*source` allocation fails at line 1017, lines 1019-1020 destroy
   `*part_ids` and `*path` without clearing them.
4. If `*path_prefix` allocation fails at line 1030, lines 1032-1034 destroy
   all previous outputs without clearing them.
5. The caller initializes the outputs at lines 1564-1567, calls the helper at
   lines 1680-1681, and later destroys every non-`NULL` value at lines
   1738-1749.

Thus, for example, a failure at line 1006 leaves `file_path` pointing to the
SDS object already destroyed at line 1008.

## Trigger

The bug requires one or more successful `cfl_sds_create()` calls followed by an
allocation failure. It is not triggered by an ordinary malformed blob record.

## Impact / severity

Severity: **Low — OOM-only availability and allocator-integrity bug**.

The common cleanup may double-free an SDS allocation and terminate the process
or corrupt allocator state. No ordinary-input UAF or remote code execution was
demonstrated.

## Proposed fix

The minimal fix clears every output immediately after destroying it. A stronger
implementation would use local temporaries and publish outputs only after all
allocations succeed.

```diff
diff --git a/plugins/out_azure_blob/azure_blob_db.c b/plugins/out_azure_blob/azure_blob_db.c
@@ -1005,7 +1005,8 @@ int azb_db_file_oldest_ready(struct flb_azure_blob *ctx,
         *part_ids = cfl_sds_create(tmp);
         if (!*part_ids) {
             cfl_sds_destroy(*path);
+            *path = NULL;
             sqlite3_clear_bindings(ctx->stmt_get_oldest_file_with_parts);
@@ -1016,8 +1017,10 @@ int azb_db_file_oldest_ready(struct flb_azure_blob *ctx,
         *source = cfl_sds_create(tmp);
         if (!*source) {
             cfl_sds_destroy(*part_ids);
+            *part_ids = NULL;
             cfl_sds_destroy(*path);
+            *path = NULL;
             sqlite3_clear_bindings(ctx->stmt_get_oldest_file_with_parts);
@@ -1029,9 +1032,12 @@ int azb_db_file_oldest_ready(struct flb_azure_blob *ctx,
             *path_prefix = cfl_sds_create(tmp);
             if (!*path_prefix) {
                 cfl_sds_destroy(*source);
+                *source = NULL;
                 cfl_sds_destroy(*part_ids);
+                *part_ids = NULL;
                 cfl_sds_destroy(*path);
+                *path = NULL;
                 sqlite3_clear_bindings(ctx->stmt_get_oldest_file_with_parts);
```

Initializing all output parameters to `NULL` on entry and using local
temporaries would further make the ownership contract explicit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6315162a8d4b1ef42b038834e639697f8cb44912`.  There
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
{"case_id": "fluent_fluent_bit__12202__6315162",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
