# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
remote::pgvector provider crashes on startup when vector extension doesn't exist in database

### System Info

- ogx v1.1.2 (also reproducible on v1.1.1)
- Python 3.12
- asyncpg 0.30+
- pgvector (Python) 0.4+
- PostgreSQL 16/18 with pgvector extension installed but not yet created (`CREATE EXTENSION vector` not run)

### Information

- [x] My own modified scripts

### 🐛 Describe the bug

The `remote::pgvector` provider crashes on startup with `ValueError: unknown type: public.vector` when the `vector` extension exists in the PostgreSQL installation but hasn't been activated with `CREATE EXTENSION vector` yet.

The provider has code to auto-create the extension (`create_vector_extension()` at line ~818 in `pgvector.py`), but this code is never reached because `asyncpg.create_pool()` runs the `init` callback (`_init_connection` → `register_vector(conn)`) on the first connection **before** the extension check runs.

**Initialization order in `_ensure_pool()`:**

```python
# Line 797 — pool creation triggers _init_connection on the first connection
pool = await asyncpg.create_pool(
    ...,
    init=self._init_connection,   # ← calls register_vector(conn)
    ...                           #    CRASHES: "unknown type: public.vector"
)

# Line 812-818 — extension creation (NEVER REACHED)
if not self._pool_initialized:
    async with pool.acquire() as conn:
        version = await check_extension_version(conn)
        if version:
            log.info(...)
        else:
            await create_vector_extension(conn)  # ← never gets here
```

**Reproduction:**

1. Start a PostgreSQL instance with the pgvector `.so` installed but without running `CREATE EXTENSION vector`
2. Configure an OGX server with `remote::pgvector` provider pointing to this database
3. Start the server

The server crashes immediately and enters a restart loop.

**Workaround:** Pre-create the extension before starting OGX:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Error logs

```
INFO     Initializing PGVector memory adapter
         config={'host': 'pgvector-service', 'port': 5432, 'db': 'pgvector',
         'user': 'pgvector_user', ...}

ERROR    Could not connect to PGVector database server

Traceback:
  File "ogx/providers/remote/vector_io/pgvector/pgvector.py", line 797, in _ensure_pool
    pool = await asyncpg.create_pool(
  File "asyncpg/pool.py", line 439, in _async__init__
  File "asyncpg/pool.py", line 466, in _initialize
  File "asyncpg/pool.py", line 153, in _connect
    self._con = await self._pool._get_new_connection()
  File "asyncpg/pool.py", line 573, in _get_new_connection
    raise ex
  File "asyncpg/pool.py", line 560, in _get_new_connection
    raise ValueError(
ValueError: unknown type: public.vector

The above exception was the direct cause of the following exception:

RuntimeError: Could not connect to PGVector database server
```

### Expected behavior

The provider should create the `vector` extension before attempting to register the type codec. The `create_vector_extension()` function already exists in the codebase — it just needs to run before `asyncpg.create_pool()` (or the `init` callback should handle the missing extension gracefully).

A possible fix would be to either:
1. Run `CREATE EXTENSION IF NOT EXISTS vector` in a standalone connection before creating the pool
2. Defer `register_vector()` from the pool `init` callback to after `create_vector_extension()` completes
3. Catch `ValueError` in `_init_connection` and retry after creating the extension
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `821115dee05d81c3f3b30ccffd2b3908a86c35f4`.  There
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
{"case_id": "ogx_ai_ogx__6164__821115d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
