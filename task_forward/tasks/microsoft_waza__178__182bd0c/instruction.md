# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Platform: SSE live events during run execution

Push real-time progress events via /api/events SSE endpoint during ADC execution. Wire Live view to show task progress, grader results, completion.\n\nPart of #168
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `182bd0c78c53fe3eff02ebb7eb8037c5d8458595`.  There
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
{"case_id": "microsoft_waza__178__182bd0c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
