# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
flb_log_cache_create: SDS allocation failure causes use-after-free

## Summary

When allocation of `entry->buf` fails, `flb_log_cache_create()` destroys the
partially built cache but continues execution. It then writes to the current
entry and accesses `cache->entries` after `cache` has been freed.

## Bug detail

Affected source:

- `src/flb_log.c:571-607`, `flb_log_cache_create()`
- `src/flb_log.c:609-626`, `flb_log_cache_destroy()`

Failure path:

1. `cache` is allocated at line 581.
2. `entry` is allocated at line 590.
3. `entry->buf = flb_sds_create_size(...)` fails at line 597.
4. Line 600 calls `flb_log_cache_destroy(cache)`.
5. The destructor frees the cache at line 625 and any previously linked entries.
6. Control continues to line 602 and writes `entry->timestamp`, then line 603
   calls `mk_list_add(..., &cache->entries)` using the freed cache.

The current `entry` has not yet been linked into the list, so it must also be
freed separately on this path to avoid a leak.

## Trigger

The cache and entry allocations must succeed while the SDS buffer allocation
fails. This requires OOM or deterministic fault injection for
`flb_sds_create_size()`.

## Impact / severity

Severity: **Low — OOM-only UAF/write-after-free and availability bug**.

The process may crash during logger initialization or corrupt allocator/list
state. No ordinary-input trigger, information disclosure, or code execution was
demonstrated.

## Proposed fix

Free the unlinked entry, destroy the cache, and return immediately:

```diff
diff --git a/src/flb_log.c b/src/flb_log.c
@@ -597,8 +597,11 @@ struct flb_log_cache *flb_log_cache_create(int timeout_seconds, int size)
         entry->buf = flb_sds_create_size(FLB_LOG_CACHE_TEXT_BUF_SIZE);
         if (!entry->buf) {
             flb_errno();
+            flb_free(entry);
             flb_log_cache_destroy(cache);
+            return NULL;
         }
         entry->timestamp = 0; /* unset for now */
```

##
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cf50b7ed3a4ca59206506e988c95b861cf94f452`.  There
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
{"case_id": "fluent_fluent_bit__12205__cf50b7e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
