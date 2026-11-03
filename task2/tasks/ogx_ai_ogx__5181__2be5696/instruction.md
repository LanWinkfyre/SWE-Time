# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Re-enable external provider CI test using llama-stack-provider-lmeval

## Summary

The external provider module test workflow (`.github/workflows/test-external-provider-module.yml`) has been disabled since it previously depended on `ramalama`, which is no longer maintained/compatible.

This issue tracks re-enabling the workflow using [`llama-stack-provider-lmeval`](https://github.com/trustyai-explainability/llama-stack-provider-lmeval) as the external provider under test.

## Changes needed

- Replace ramalama with `llama-stack-provider-lmeval` as the external provider
- Use `remote::ollama` as the inference provider dependency (lmeval requires an inference API)
- Set `TRUSTYAI_LMEVAL_USE_K8S=false` to avoid needing Kubernetes in CI
- Remove the `if: false` guard to re-enable the workflow
- Simplify server readiness check to use `/v1/health` endpoint
- Add a step to verify the external provider is registered via `/v1/providers`

## Purpose

This test validates that the external provider installation mechanism works end-to-end: a provider installed via `pip install` can be loaded by the llama-stack server at startup.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2be5696e073a6620f64ab9af8770dacb64e2f765`.  There
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
{"case_id": "ogx_ai_ogx__5181__2be5696",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
