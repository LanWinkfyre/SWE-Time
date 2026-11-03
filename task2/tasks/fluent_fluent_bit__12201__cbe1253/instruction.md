# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
oauth2: allocation failure in `oauth2_append_kv()` can double-free the request body

## Summary

`oauth2_append_kv()` frees the SDS buffer passed by `oauth2_build_body()` when
URI encoding or SDS concatenation fails, then returns `NULL`. The caller still
executes `flb_sds_destroy(body)`, so the same allocation can be destroyed twice.

## Bug detail

Affected source:

- `src/flb_oauth2.c:584-642`, `oauth2_append_kv()`
- `src/flb_oauth2.c:1000-1088`, `oauth2_build_body()`

The failure path is:

1. `oauth2_build_body()` allocates `body` at line 1000.
2. It passes `body` to `oauth2_append_kv()` at lines 1005, 1013, 1022,
   1031, 1041, 1050, 1060, 1068, or 1082.
3. `oauth2_append_kv()` calls `flb_uri_encode()` at line 592. If it fails,
   the function destroys `buffer` at lines 595-597 and returns `NULL`.
4. If an SDS append fails at lines 602, 613, 623, or 633, the function also
   destroys the current `buffer` at lines 606, 617, 627, or 636-638 and
   returns `NULL`.
5. The caller then destroys `body` at lines 1007, 1015, 1024, 1033, 1043,
   1052, 1062, 1071, or 1085.

`flb_sds_cat()` may reallocate the SDS object before a later append fails, so
the callee's cleanup is also the reason the original caller pointer may be
stale. The ownership contract between the two functions is therefore unsafe.

## Trigger

The issue requires failure of `flb_uri_encode()` or `flb_sds_cat()`. The input
strings are OAuth2 configuration values such as `client_id`, `client_secret`,
`scope`, `audience`, and `resource`; their lengths can influence allocation
sizes, but a normal remote log payload does not directly control these fields.

## Impact / severity

Severity: **Low — OOM-only availability and allocator-integrity bug**.

On the failure path, the process may abort in the allocator or terminate while
handling an OAuth2 token refresh. No ordinary-input UAF or code execution was
demonstrated. Triggering it requires resource exhaustion or deterministic
allocator fault injection.

## Proposed fix

The smallest fix is to keep the existing ownership convention in
`oauth2_append_kv()` and stop destroying `body` again in the callers. A cleaner
API would pass `flb_sds_t *` and make ownership explicit, but the following
minimal patch prevents the double-free:

```diff
diff --git a/src/flb_oauth2.c b/src/flb_oauth2.c
@@ -1003,7 +1003,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
     tmp = oauth2_append_kv(body, "grant_type", "client_credentials");
     if (!tmp) {
-        flb_sds_destroy(body);
         return NULL;
     }
@@ -1012,7 +1011,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
         tmp = oauth2_append_kv(body, "scope", ctx->cfg.scope);
         if (!tmp) {
-            flb_sds_destroy(body);
             return NULL;
         }
@@ -1021,7 +1019,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
         tmp = oauth2_append_kv(body, "audience", ctx->cfg.audience);
         if (!tmp) {
-            flb_sds_destroy(body);
             return NULL;
         }
@@ -1030,7 +1027,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
         tmp = oauth2_append_kv(body, "resource", ctx->cfg.resource);
         if (!tmp) {
-            flb_sds_destroy(body);
             return NULL;
         }
@@ -1040,7 +1036,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
             tmp = oauth2_append_kv(body, "client_id", ctx->cfg.client_id);
             if (!tmp) {
-                flb_sds_destroy(body);
                 return NULL;
             }
@@ -1049,7 +1044,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
             tmp = oauth2_append_kv(body, "client_secret", ctx->cfg.client_secret);
             if (!tmp) {
-                flb_sds_destroy(body);
                 return NULL;
             }
@@ -1059,7 +1053,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
             tmp = oauth2_append_kv(body, "client_id", ctx->cfg.client_id);
             if (!tmp) {
-                flb_sds_destroy(body);
                 return NULL;
             }
@@ -1068,7 +1061,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
         tmp = oauth2_append_kv(body, "client_assertion_type",
                                "urn:ietf:params:oauth:client-assertion-type:jwt-bearer");
         if (!tmp) {
-            flb_sds_destroy(body);
             return NULL;
         }
@@ -1081,7 +1073,6 @@ static flb_sds_t oauth2_build_body(struct flb_oauth2 *ctx)
         flb_sds_destroy(assertion);
         if (!tmp) {
-            flb_sds_destroy(body);
             return NULL;
         }
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cbe12539d4fab7e332463abac75836f82ce46a39`.  There
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
{"case_id": "fluent_fluent_bit__12201__cbe1253",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
