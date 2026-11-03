# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Expose httpx connection pool config for inference providers

### 🚀 Describe the new functionality needed

Currently, all inference providers use `httpx` for making requests, but none expose `httpx.Limits`. Because of this, the defaults below are always used:

```python
class Limits:
    def __init__(
        self,
        *,
        max_connections: int | None = 100,
        max_keepalive_connections: int | None = 20,
        keepalive_expiry: float | None = 5.0,
    ):
    ...
```

These should be configurable through each inference provider's network config.

### 💡 Why is this needed? What if we don't build it?

Connection pooling configuration is a standard http client concern that should be configurable by platform admins. Without it, the default values of 100 max connections (20 keepalive) can cause performance bottlenecks with many concurrent requests.

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ebaaff8b17b8e3a7190c7b26565eda111659336c`.  There
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
{"case_id": "ogx_ai_ogx__5910__ebaaff8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
