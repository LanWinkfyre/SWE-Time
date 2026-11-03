# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
[Docs] Mismatch between Gemini provider docs and code behavior

### System Info

N/A

### Information

- [x] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

Per https://github.com/ogx-ai/ogx/blob/main/src/ogx/providers/remote/inference/gemini/config.py#L49 at the time of writing 
```python
        if has_api_key and has_access_token:
            raise ValueError("api_key and access_token are mutually exclusive — set one or the other, not both")
```

however, the [gemini docs](https://ogx-ai.github.io/docs/providers/inference/remote_gemini) state
```
OAuth2 access token for Gemini. When set, used instead of api_key for Bearer authentication.
```


### Error logs

N/A

### Expected behavior

Docs and code should match
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4a9b9983a64c93593971a6e78c4f874bd9b2afe1`.  There
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
{"case_id": "ogx_ai_ogx__5970__4a9b998",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
