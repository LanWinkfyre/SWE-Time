# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Restore Hermes forwards before interactive launch (PR #11578)

Parent epic: #11573

## Outcome

Restore receipt-scoped Hermes forwards before opening the interactive connection.

## Pull request

- PR: #11578
- Verified commit: [`e54553c38`](https://github.com/NVIDIA/NemoClaw/commit/e54553c380af5ec71de9cc27e499ed7f11700106)

## Defect

Interactive Hermes launch could proceed before its required forwards were restored, leaving the TUI unable to reach the expected service even though lifecycle recovery had otherwise succeeded.

## Completion

- [x] Open and link a focused PR to `main`.
- [x] Pass the 57-test connect-flow suite, CLI build, and CLI type-check.
- [ ] Pass full CI and review.
- [ ] Record the merged `main` commit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `70cfff5f946a9bb31d1147f78ffbda914a2efaa2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11567__70cfff5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
