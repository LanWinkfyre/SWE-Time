# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Auth middleware breaks public routes (health, version) on FastAPI >= 0.137

FastAPI 0.137 changed `include_router()` to store routers as a tree (`_IncludedRouter`) instead of flattening all routes into `app.router.routes` as `APIRoute` objects.

`build_route_impls_from_routes()` in `src/ogx/core/server/routes.py` iterates `app.router.routes` and filters with `isinstance(route, APIRoute)`. On FastAPI 0.137+ this matches nothing, so the auth middleware has an empty route table, never sees `openapi_extra={PUBLIC_ROUTE_KEY: True}` on `/v1/health` or `/v1/version`, and requires authentication on all endpoints.

Symptom: `GET /v1/health` returns 401 instead of 200 when authentication is configured.

Ref: https://github.com/fastapi/fastapi/releases/tag/0.137.0
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c4f8f6dcb88db55ea23c2c98a26c0a855eb7d14f`.  There
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
{"case_id": "ogx_ai_ogx__6265__c4f8f6d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
