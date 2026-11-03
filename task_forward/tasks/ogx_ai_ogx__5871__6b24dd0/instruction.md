# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Add `ogx connect` support for Codex

### 🚀 Describe the new functionality needed

Followup from https://github.com/ogx-ai/ogx/pull/5675

We have a new command subgroup `ogx connect` that allows OGX to connect with third-party services directly

Extend our Codex support to utilize this new command subgroup

### 💡 Why is this needed? What if we don't build it?

Improved UX for users using Codex with OGX, better integration with external tools

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6b24dd068871f7b1759fc6665d8bebd0eccc96a5`.  There
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
{"case_id": "ogx_ai_ogx__5871__6b24dd0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
