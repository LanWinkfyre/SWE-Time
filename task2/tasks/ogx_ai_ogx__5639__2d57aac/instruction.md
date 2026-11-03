# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Make OGX a provider for OpenCode

### 🚀 Describe the new functionality needed

[OpenCode](https://opencode.ai/) is a popular, open source project that provides a Claude-like Terminal-based interface for interacting with models

We should explore making OGX a [provider](https://opencode.ai/docs/providers) for OpenCode

### 💡 Why is this needed? What if we don't build it?

Inter-project collaboration, drive adoption of OGX

### Other thoughts

Could try this out by using an OGX endpoint as a [custom provider](https://opencode.ai/docs/providers/#custom-provider)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2d57aacb987e484a90441ac0a9d86439298a5820`.  There
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
{"case_id": "ogx_ai_ogx__5639__2d57aac",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
