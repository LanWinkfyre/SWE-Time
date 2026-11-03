# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
embedding: global sentence-transformer cache ignores trust_remote_code setting

## Summary

The process-global `SentenceTransformer` cache in `embedding_mixin.py` is keyed only by model name, ignoring the `trust_remote_code` parameter. When multiple provider instances load the same model with different `trust_remote_code` values, whichever loads first wins - later requests silently reuse the cached object regardless of their security configuration.

## Impact

A provider configured with `trust_remote_code=False` could receive a model object that was loaded with `trust_remote_code=True`, bypassing its intended security restriction against executing arbitrary remote code from HuggingFace model repos. The reverse is also broken: a `False`-first load prevents a later `True` config from loading the model with its required custom code.

In practice this would require a distribution running multiple `inline::sentence-transformers` provider instances with different `trust_remote_code` settings for the same model. This is an unusual but valid configuration.

## Reproduction

1. Configure two `inline::sentence-transformers` provider instances for the same model, one with `trust_remote_code=True` and one with `trust_remote_code=False`
2. Load the model via the `True` provider first
3. Load the model via the `False` provider - it silently returns the `True`-loaded object

## Fix

Changed the cache key from `model` (str) to `(model, trust_remote_code)` (tuple) so different security configurations get separate cache entries.

**PR:** https://github.com/ogx-ai/ogx/pull/5928

**Parent issue:** #5906
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
{"case_id": "ogx_ai_ogx__5929__11c174c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
