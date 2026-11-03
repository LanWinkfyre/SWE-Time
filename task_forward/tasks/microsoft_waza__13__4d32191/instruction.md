# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Eval & Grader Registry — design doc

> _Migrated from [spboyer/waza#385](https://github.com/spboyer/waza/issues/385)_

## Summary

Design a shared eval and grader registry for waza — inspired by OpenAI Evals' 800+ community registry but adapted for agent evaluation.

## Context

From `docs/research/waza-vs-openai-evals.md`, the registry gap is waza's #1 competitive disadvantage (Row 10). This epic covers the full design.

## Sub-issues

- [ ] #386 — Map OpenAI Evals format to waza graders
- [ ] #387 — Design Go-module-style grader/eval references
- [ ] #388 — Evaluate registry backend options (Git/OCI/Releases/federated)
- [ ] #389 — Design composable eval construction
- [ ] #390 — Grader plugin extensibility design (WASM/external)

## Peter's Ideas (verbatim)

- The registry of shared evals is interesting. Graders particularly.
- OpenAI's are all in their repo as YAML files
- Consuming their format could be interesting
- Go module style: just point to a repo and that is your grader or eval
- Being able to construct your eval from a set of known graders is interesting

## Deliverable

Design document at `docs/research/waza-eval-registry-design.md` — design only, no implementation.

## Non-goals (for now)

- Implementation — this is design research only
- NOT a single JSON file for the registry — needs to be more robust
- Not building the actual CLI commands yet
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4d32191c5ab71e6772acc0e7e154620821c38746`.  There
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
{"case_id": "microsoft_waza__13__4d32191",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
