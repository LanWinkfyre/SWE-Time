# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Select one lifecycle lock authority after the HOME fence (PR #11490)

Parent epic: #11573

## Delivered outcome

Use one host-scoped Hermes Portable lifecycle-lock policy and select its lock domain only after acquiring the current HOME fence.

## Pull request

- Merged PR: #11490
- Merge commit: [`41a54ca4e`](https://github.com/NVIDIA/NemoClaw/commit/41a54ca4eb51726942d369bab436ed6a3949b10f)

## Defects addressed

- Lock policy was duplicated across start, stop, launch, connect, status, doctor, and recovery paths.
- A lifecycle caller could choose a gateway or receipt lock domain before waiting for the HOME fence, allowing the relevant receipt state to change underneath that decision.
- Direct synchronous Portable lifecycle calls could enter the receipt lock without the outer host fence.

## Changes delivered

- Centralize Portable receipt classification and host-scoped lock selection.
- Acquire the Portable HOME fence before selecting and entering the lifecycle lock.
- Require synchronous Portable callers to already hold the host fence and fail closed otherwise.
- Preserve the existing gateway-scoped behavior for ordinary non-Portable sandboxes.

Status: delivered to `main`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e13e1a025f3f524d1669069844cd3a1073cdfa73`.  There
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
{"case_id": "NVIDIA_NemoClaw__11561__e13e1a0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
