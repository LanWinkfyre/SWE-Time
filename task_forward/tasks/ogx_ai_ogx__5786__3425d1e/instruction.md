# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Models from disabled providers persist in Postgres registry after restart

## Bug

When OGX is started with a provider (e.g., OpenAI), models are auto-discovered and registered in the Postgres KV store. When the server is restarted with that provider **disabled** (env var unset), the stale models remain in `/v1/models`.

This is a re-report of #3150, which was auto-closed for inactivity without being fixed. The attempted fix in #3198 was closed without merge (needed rebase).

## Steps to reproduce

Using the upstream `starter` distribution with `run-with-postgres-store.yaml`:

```bash
# Prerequisites: PostgreSQL on localhost:5432, OPENAI_API_KEY set, uv installed

# 1. Create a fresh database
psql -U postgres -c "CREATE DATABASE ogx_repro;"

# 2. Start OGX with OpenAI provider enabled
export POSTGRES_DB=ogx_repro POSTGRES_USER=postgres POSTGRES_PASSWORD=...
uvx --python 3.12 --from 'ogx[starter]' --with botocore \
  ogx stack run starter --port 8322

# 3. Verify OpenAI models are discovered
curl -s http://localhost:8322/v1/models | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
bp={}
for m in d:
    p=m['custom_metadata']['provider_id']
    bp[p]=bp.get(p,0)+1
print(f'{len(d)} total models')
for p,c in sorted(bp.items()):
    print(f'  {p}: {c}')
"
# Output: 140 total models
#   openai: 138
#   sentence-transformers: 1
#   transformers: 1

# 4. Stop the server (Ctrl+C or kill)

# 5. Restart WITHOUT OpenAI (unset the key)
OPENAI_API_KEY="" uvx --python 3.12 --from 'ogx[starter]' --with botocore \
  ogx stack run starter --port 8322

# 6. Check models again
curl -s http://localhost:8322/v1/models | python3 -c "..."
# Output: 140 total models   <-- BUG: still 138 openai models
#   openai: 138
#   sentence-transformers: 1
#   transformers: 1
```

## Expected behavior

After restart with `OPENAI_API_KEY=""`, the OpenAI provider is not configured (`provider_id` resolves to empty via `${env.OPENAI_API_KEY:+openai}`). The `/v1/models` endpoint should return only models from active providers (sentence-transformers, transformers).

**Expected:** 2 models (sentence-transformers + transformers)

## Actual behavior

**Actual:** 140 models — the 138 OpenAI models persist in the Postgres `ogx_kvstore` table under the `registry` namespace and are served on subsequent startups regardless of provider configuration.

## Root cause

Auto-discovered models are persisted in the Postgres KV store (`registry` namespace) during `list_models()` / model refresh. On restart, the registry is loaded from Postgres without cross-checking whether the provider that registered each model is still active. There is no cleanup mechanism for stale entries when provider configuration changes.

## Environment

- OGX version: 0.7.2 (PyPI, via `uvx --from 'ogx[starter]'`)
- Storage: PostgreSQL 17 (kv_postgres backend)
- Config: `run-with-postgres-store.yaml` (bundled starter distribution)
- OS: Fedora 43 (Linux 6.19)

## Related

- #3150 — original report (auto-closed for inactivity, not fixed)
- #3198 — attempted fix (closed without merge, needed rebase)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3425d1e623ebb6b738cad26d75d6a5b1583b1a20`.  There
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
{"case_id": "ogx_ai_ogx__5786__3425d1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
