# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Linux][Docs] Recover and Rebuild Sandboxes omits active host-forward recovery prerequisite from Deep Agents variant

## Description

The published Recover and Rebuild Sandboxes guidance is inconsistent across product documentation variants. The OpenClaw and Hermes variants document that an already active host forward is only accepted after OpenShell ownership reconciliation and local endpoint reachability are satisfied, but the Deep Agents variant omits that recovery prerequisite.

Platform scope: Reproduced on Linux only; other platforms not tested. The defect is in published documentation variants, not in a Linux-only runtime path.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No.

## Environment

```text
Device:        DGX Spark test system
OS:            Ubuntu 24.04
Architecture:  aarch64
Node.js:       Not required for this documentation validation
npm:           Not required for this documentation validation
Docker:        Available on the test system
OpenShell CLI: Present through NemoClaw v0.0.119 workflow
NemoClaw:      v0.0.119
OpenClaw:      Not required for this prose-only documentation validation
```

## Steps to Reproduce

1. Open the published Recover and Rebuild Sandboxes pages for OpenClaw, Hermes, and Deep Agents.
2. Search each variant for the active host-forward recovery prerequisite.
3. Specifically compare whether each page says that an already active host forward is accepted only after OpenShell ownership is reconciled and the local endpoint is reachable.

## Expected Result

All three published variants should document the same active host-forward recovery prerequisite, because users of each product variant can encounter the same gateway and host-forward recovery condition.

## Actual Result

The OpenClaw and Hermes variants include the active host-forward recovery prerequisite. The Deep Agents variant omits the equivalent prerequisite, leaving Deep Agents users without the required recovery guidance.

## Logs

```text
Published OpenClaw page: required active host-forward recovery sentence present.
Published Hermes page: required active host-forward recovery sentence present.
Published Deep Agents page: required active host-forward recovery sentence absent.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3e605bc55b4a660b03bf1e132bdd9725078e346c`.  There
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
{"case_id": "NVIDIA_NemoClaw__11176__3e605bc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
