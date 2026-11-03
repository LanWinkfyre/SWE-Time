# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Missing ABAC test coverage for openai_create_vector_store

## Context

Sub-issue of #5906 (Clawpatch finding: "ABAC enforcement missing for openai_create_vector_store").

## Finding

The Clawpatch audit reported this as a security bug, but investigation shows the production code is **not vulnerable**. The ABAC check exists in `CommonRoutingTableImpl.register_object()` (`src/ogx/core/routing_tables/common.py:196`) which calls `is_action_allowed("create", obj, creator)` before persisting the resource.

The create path uses a different enforcement mechanism than other operations:
- **Read/update/delete**: routing table methods call `assert_action_allowed()` which looks up an existing resource by ID
- **Create**: `register_object()` calls `is_action_allowed()` directly on the in-memory object (since the resource doesn't exist yet to look up)

The ABAC test suite (`test_vector_stores_abac.py`) parametrizes 15 operations and spies on `assert_action_allowed`, but since create goes through a different code path, it was omitted - leaving a real test gap even though the production code is secure.

Verified by running the server with Keycloak auth and an access_policy that omits the `create` permit rule - the server correctly returns `AccessDeniedError`.

## Fix

Add `test_register_object_enforces_abac_on_create` to verify that `register_object` checks `is_action_allowed("create", ...)` and raises `AccessDeniedError` when the policy denies access.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `83ed3173cd8a0293fd9a62d49908edac9f4684e3`.  There
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
{"case_id": "ogx_ai_ogx__5933__83ed317",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
