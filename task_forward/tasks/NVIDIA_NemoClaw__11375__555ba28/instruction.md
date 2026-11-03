# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Document the external-component lifecycle contract

## Description

PR #11366 implements the experimental v1 external-component lifecycle accepted in #11340. NemoClaw's public documentation does not yet explain how an operator registers a component or how the bounded activation result affects onboarding.

## Affected Page

No current page owns this contract. Route the merged behavior through the post-merge documentation workflow and place it with the owning onboarding guidance.

## Issue Type

Missing documentation

## Suggested Fix

After #11366 merges, document only the shipped v1 contract:

- the fixed declaration path, exact secret-free fields, ownership, mode, and Unix socket requirements;
- supported Linux, fresh sandbox, and NemoClaw-managed gateway limits;
- NemoClaw's fixed interceptor settings and sole gateway-writer authority;
- the exact HTTP activation request and response, fixed 30-second deadline, and no automatic retry;
- identity and effective-policy verification before handoff and after activation;
- preserved sandbox and bounded incomplete-state evidence after failed or ambiguous activation;
- credential exclusion and unsupported resume, rebuild, recreation, migration, and externally supervised gateway behavior.

Derive the text from the merged implementation and validate it with the documentation workflow. Do not document unmerged or speculative behavior.

Refs #11340
Follow-up to #11366
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `555ba281feb4924935bda74dc35baa42129218fe`.  There
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
{"case_id": "NVIDIA_NemoClaw__11375__555ba28",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
