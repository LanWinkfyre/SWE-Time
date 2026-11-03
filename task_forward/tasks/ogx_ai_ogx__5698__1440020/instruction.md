# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug(auth): OAuth2 introspection ignores verify_tls setting

## Summary

`OAuth2TokenAuthProvider` in `src/ogx/core/server/auth_providers.py` (lines 224-228) defaults to `verify=False` for introspection requests unless `tls_cafile` is explicitly set. The `verify_tls` config field is not consulted for introspection calls, unlike the JWKS flow which correctly handles it (lines 153-163).

This means an enterprise deployment with `verify_tls=True` (the default) still makes unverified introspection calls, creating a MITM risk.

## Current behavior

```python
# auth_providers.py:224-228
ssl_ctxt: ssl.SSLContext | bool = False
if self.config.tls_cafile:
    ssl_ctxt = ssl.create_default_context(cafile=str(self.config.tls_cafile))
```

When `tls_cafile` is not set, `ssl_ctxt` stays `False`, which means `verify=False` in the httpx call. The `verify_tls` field from config is never checked in this code path.

## Expected behavior

Introspection should respect `verify_tls`:
- `verify_tls=True` (default) + no `tls_cafile` → use system CA bundle (`verify=True`)
- `verify_tls=True` + `tls_cafile` → use custom CA
- `verify_tls=False` → skip verification with a WARNING log

The JWKS code path at lines 153-163 already implements this pattern correctly and can serve as a reference.

## Impact

Enterprise deployments using OAuth2 token introspection with default TLS settings are silently making unverified HTTP calls to the introspection endpoint.

## Test plan

Add test cases in `tests/unit/server/` that assert:
- Introspection request uses `verify=True` by default
- Custom CA file is applied when configured
- `verify_tls=False` disables verification
- WARNING is logged when verification is disabled
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
{"case_id": "ogx_ai_ogx__5698__1440020",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
