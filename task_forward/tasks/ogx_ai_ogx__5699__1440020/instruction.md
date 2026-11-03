# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug(storage): PostgreSQL keys_in_range() returns expired rows

## Summary

In `src/ogx/core/storage/kvstore/postgres/postgres.py` (lines 118-127), `keys_in_range()` does not filter expired rows, unlike `get()` (lines 80-92) and `values_in_range()` (lines 102-116) which both exclude expired entries.

This creates an inconsistency where key enumeration returns stale entries that would return nothing if fetched individually.

## Current behavior

```python
# get() - filters expired (correct)
async def get(self, key: str) -> str | None:
    # ... includes: AND (expiration IS NULL OR expiration > NOW())

# values_in_range() - filters expired (correct)
async def values_in_range(self, start_key, end_key):
    # ... includes: AND (expiration IS NULL OR expiration > NOW())

# keys_in_range() - does NOT filter expired (bug)
async def keys_in_range(self, start_key, end_key):
    # ... no expiration filter
```

## Expected behavior

`keys_in_range()` should include the same expiration filter as `get()` and `values_in_range()`.

## Impact

Any code that enumerates keys (e.g., for cleanup, migration, or quota accounting) will see expired entries that no longer resolve via `get()`. This can cause phantom key counts and stale iteration results.

## Additional context

Redis KV has a related but different inconsistency: its range upper bound is inclusive (`<= end_key`) while PostgreSQL uses exclusive (`< end_key`). The KV store interface does not specify which behavior is correct. Cross-backend consistency should be documented or enforced.

## Test plan

Add `tests/unit/core/storage/kvstore/test_postgres_kvstore.py`:
- Set a key with short expiration, wait, verify `keys_in_range()` excludes it
- Verify `keys_in_range()` and `values_in_range()` return the same key set
- Verify range bound behavior (inclusive vs exclusive) matches `values_in_range()`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1440020909e3ad59100e494b4aaee0fce91b647b`.  There
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
{"case_id": "ogx_ai_ogx__5699__1440020",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
