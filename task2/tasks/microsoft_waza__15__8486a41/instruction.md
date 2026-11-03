# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Go-module-style grader/eval references

> _Migrated from [spboyer/waza#387](https://github.com/spboyer/waza/issues/387)_

## Summary

Design how eval.yaml can reference remote graders via Go-module-style paths.

## Concept

```yaml
graders:
  - ref: github.com/waza-evals/fact@v1.0
  - ref: github.com/myorg/custom-grader@v2.1
    config:
      threshold: 0.8
```

## Design Questions

- How does `waza get` resolve and cache remote graders?
- Version pinning semantics (exact, range, latest)?
- Offline/air-gapped fallback from local cache?
- How to handle transitive dependencies (grader A depends on dataset B)?
- Authentication for private repos?

## Parent: #385
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8486a419ada4b4bb6c31451e665ff170045a5dd2`.  There
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
{"case_id": "microsoft_waza__15__8486a41",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
