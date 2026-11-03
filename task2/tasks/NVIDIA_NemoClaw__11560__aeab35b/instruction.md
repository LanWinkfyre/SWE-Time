# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Rollback partial Hermes starts and unify lifecycle lock roots (PR #11482)

Parent epic: #11573

## Delivered outcome

Use the receipt-scoped lifecycle lock consistently across start, stop, provider recovery, and connect, and roll back an exact container when OpenShell start changes state before reporting failure.

## Pull request

- Merged PR: #11482
- Merge commit: [`e13e1a025`](https://github.com/NVIDIA/NemoClaw/commit/e13e1a025f3f524d1669069844cd3a1073cdfa73)

## Defects addressed

- Start, stop, and interactive connect could still choose different lock roots after #11336.
- A nonzero or errored OpenShell start could leave the exact container running without entering rollback.

## Changes delivered

- Centralize receipt-scoped lifecycle-lock selection for the affected command and provider paths.
- Reconcile exact container state after a failed start mutation and stop it when the failed operation started it.
- Add non-default-port connect/stop and partial-start rollback coverage.

Status: delivered to `main`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `aeab35b84c75c968b0b9b4e03f63ed2e6591ae00`.  There
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
{"case_id": "NVIDIA_NemoClaw__11560__aeab35b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
