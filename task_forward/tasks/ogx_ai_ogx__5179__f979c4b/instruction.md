# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Auto-record integration tests on PRs with multi-provider support

## Summary

Add automated recording of missing integration test fixtures when PRs are opened or updated, with support for multiple providers.

## Motivation

Currently, adding or modifying integration tests requires manually recording test fixtures. This is error-prone and slows down the PR workflow. Automating this process ensures recordings are always up to date and reduces friction for contributors.

## Scope

- Auto-trigger recording on PRs that touch `tests/integration/` or `src/llama_stack/` (ollama only, no secrets exposed to forks)
- Manual `workflow_dispatch` for providers requiring API keys (gpt, azure, bedrock, etc.)
- Fork PR support with automatic commits via GitHub API (when "Allow edits from maintainers" is enabled)
- Enhanced `run-and-record-tests` composite action
- PR comment summary with workflow run link
- Docker env var passthrough for all providers

Tracking PR: #5123
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f979c4b00219de2f93e3f60f655f7e5e2cf51d9f`.  There
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
{"case_id": "ogx_ai_ogx__5179__f979c4b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
