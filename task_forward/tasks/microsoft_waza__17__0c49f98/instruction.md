# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Composable eval construction from registry graders

> _Migrated from [spboyer/waza#389](https://github.com/spboyer/waza/issues/389)_

## Summary

Design how users construct eval.yaml from a catalog of shared, versioned grader definitions.

## Concept

Users should be able to:
1. Browse available graders (`waza registry search 'factual'`)
2. Add a grader to their eval (`waza registry add github.com/waza-evals/fact@v1.0`)
3. Reference it in eval.yaml with local config overrides
4. Run evals that mix local and remote graders seamlessly

## Design Questions

- What does `waza registry search` look like? Metadata format?
- How do remote graders interact with local graders in the same eval?
- Can you override config on a remote grader (e.g., change threshold)?
- How does `waza init` scaffold with registry graders?

## Parent: #385
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0c49f983ae3f327ad835fd90f1e9bd1819e862e7`.  There
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
{"case_id": "microsoft_waza__17__0c49f98",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
