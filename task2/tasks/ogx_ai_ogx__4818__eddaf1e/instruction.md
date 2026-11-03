# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
use the new OpenResponses CLI in the conformance test

### 🤔 What is the technical debt you think should be addressed?

we currently diff the OpenResponses spec against ours using oasdiff. The OpenResponses project recently added a CLI in https://github.com/openresponses/openresponses/pull/17, we should use this as a way of actually running the compliance tests in our CI. these tests should xfail since there are currently gaps we need to close in our Responses implementation.

### 💡 What is the benefit of addressing this technical debt?

This test will allow us to more easily keep track of our progress of conforming to open responses.

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `eddaf1e1e9629c240ed9562e1429d0dc27b75c79`.  There
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
{"case_id": "ogx_ai_ogx__4818__eddaf1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
