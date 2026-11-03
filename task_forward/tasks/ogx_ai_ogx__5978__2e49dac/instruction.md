# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Support `ssl_mode` and `ca_cert_path` in PostgreSQL SQL store config

### 🚀 Describe the new functionality needed

Hey:) 👋

Following up on #3181 the KV Postgres store (`PostgresKVStoreConfig`) already supports `ssl_mode` and `ca_cert_path` [1], but the SQL Postgres store (`PostgresSqlStoreConfig`) doesn't have these options at all [2].

[1] https://github.com/ogx-ai/ogx/blob/34d7901edcd5e81c6df796ad2cdab5db31a32f3b/src/ogx/core/storage/datatypes.py#L93
[2] https://github.com/ogx-ai/ogx/blob/34d7901/src/ogx/core/storage/datatypes.py#L200

### 💡 Why is this needed? What if we don't build it?

Without this, users connecting to Postgres instances that require TLS can configure it for the KV store but the SQL store is stuck with the default `sslmode=prefer` [1] behavior and no way to specify a CA certificate. 

[1] https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.connect

### Other thoughts

The KV store already has a `_build_ssl()` [2] helper that constructs an `ssl.SSLContext` from these config fields and passes it to `asyncpg.create_pool()`. The SQL store could reuse the same approach. Pass the SSL context via `connect_args` on SQLAlchemy's `create_async_engine` [1].

[1] https://github.com/ogx-ai/ogx/blob/34d7901/src/ogx/core/storage/sqlstore/sqlalchemy_sqlstore.py#L125
[2] https://github.com/ogx-ai/ogx/blob/34d7901edcd5e81c6df796ad2cdab5db31a32f3b/src/ogx/core/storage/kvstore/postgres/postgres.py#L36
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2e49dac1afb7c5b7abc27b651b810f2fe75215c6`.  There
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
{"case_id": "ogx_ai_ogx__5978__2e49dac",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
