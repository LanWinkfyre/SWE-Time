# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
security: upsert bypasses authorization check and overwrites record ownership

Parent: #5906 (Clawpatch audit finding `fnd_sig-feat-service-05508a04d8-917f_e7858fba44`)

## Problem

`AuthorizedSqlStore.upsert()` has two security gaps compared to `update()`:

1. No `_check_access_for_rows` call - any user can upsert against a record they don't own
2. Ownership fields (`owner_principal`, `access_attributes`) are included in the update columns on conflict, allowing User B to silently take ownership of User A's record

## Repro

1. User A inserts record `{id: '1', data: 'secret'}` - `owner_principal='userA'`
2. User B calls upsert with `{id: '1', data: 'hijacked'}`, `conflict_columns=['id']`
3. Record now has `owner_principal='userB'` - no `AccessDeniedError` raised
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `11c174c9b1a351b1db382ee85604670a7061edcd`.  There
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
{"case_id": "ogx_ai_ogx__5930__11c174c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
