# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug(auth): GitHub auth provider never fetches org/team memberships

## Summary

`GitHubTokenAuthProvider` in `src/ogx/core/server/auth_providers.py` (lines 412-427) only fetches the `/user` endpoint from GitHub's API. However, the default claims mapping in `src/ogx/core/datatypes.py` (line 278) expects an `organizations` field for attribute-based access control.

Since `/user` does not return organization memberships, the default claims mapping for GitHub auth silently produces no org/team attributes. Any access control rules based on GitHub org membership are effectively broken.

## Current behavior

```python
# auth_providers.py:412-427
async def _get_github_user_info(self, token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{self.config.github_api_url}/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
    # ... returns user info without org data
```

The default claims mapping expects:
```python
# datatypes.py:278
# organizations → user attributes
```

But `/user` response does not include `organizations`. The GitHub API requires separate calls to `/user/orgs` and `/user/teams`.

## Expected behavior

Either:
1. Fetch org/team memberships via additional API calls (`/user/orgs`, `/user/teams`)
2. Or document that the default claims mapping for organizations does not work and users must configure custom claims

## Impact

GitHub-based RBAC using org/team membership silently fails. Users configure org-based access rules that appear to work (no errors) but never match because the org data is never fetched.

## Test plan

- Mock `/user` and `/user/orgs` endpoints, verify org attributes are populated
- Test with default claims mapping, verify organizations are present
- Test failure handling when org endpoint is unavailable
- Test with user who belongs to multiple orgs
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
{"case_id": "ogx_ai_ogx__5702__1440020",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
