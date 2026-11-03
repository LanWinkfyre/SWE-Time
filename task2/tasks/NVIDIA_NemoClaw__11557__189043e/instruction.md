# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Reuse exact-owned Hermes forwards during onboarding and resume (PR #11427)

Parent epic: #11573

## Delivered outcome

Repeated Hermes onboarding and resume retain verified dashboard and API forwards on their registered ports. Missing forwards are restored; sibling reservations, foreign listeners, changed identity, and unsafe ownership fail closed.

## Pull request

- Merged PR: #11427
- Merge commit: [`b40cc623d`](https://github.com/NVIDIA/NemoClaw/commit/b40cc623d0db0d1fa44959ccb54b9f08e4f5bfd5)

## Relationship to the Portable candidate

Candidate commit [`30ef9ec7a`](https://github.com/NVIDIA/NemoClaw/commit/30ef9ec7a198270b9524ddaa8c4d0aef9b0da918) independently addressed the occupied-forward failure found in the seat cycle. It is not an ancestor of current `main`; #11427 delivered the reviewed, broader implementation and is the source of truth.

Status: delivered to `main` by #11427.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `189043e740fdab61c8c3fdf6fe9407f438e4d955`.  There
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
{"case_id": "NVIDIA_NemoClaw__11557__189043e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
