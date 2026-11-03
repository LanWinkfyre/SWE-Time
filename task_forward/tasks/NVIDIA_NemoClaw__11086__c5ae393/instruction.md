# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(network): denied host-gateway probe no longer exposes HTTP 403

## Investigation Summary

- The exact-candidate [PR #11071 E2E run](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) tested commit `0ddc3ea52efe8a5d63099b92f43cbe0a43c88a01`.
- [Network policy](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750985) passed one scenario and failed the live host-gateway allow/deny scenario.
- The denied probe returned a JSON detail beginning with `GET host.openshell.internal...`, but the assertion expected the response text to contain HTTP status `403`.

## Description

The live policy update still denies the unapproved host-gateway port, but the target cannot prove the expected denial contract because the response shape no longer includes the asserted HTTP status text.

Expected: product behavior and the E2E assertion share one stable, machine-checkable denial result.

Actual: the target sees a denial detail but fails its `403` text assertion.

## Acceptance Criteria

- Record the full redacted denial response and status separately.
- Decide whether the stable contract is the HTTP status, the structured denial detail, or both.
- Keep a negative assertion that proves the unapproved port remains inaccessible.
- Keep the approved-port assertion and the no-sandbox-restart assertion.
- The complete network-policy target passes on the fixing commit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c5ae393a02d5ba07a30e57e789c3c646fc250c36`.  There
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
{"case_id": "NVIDIA_NemoClaw__11086__c5ae393",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
