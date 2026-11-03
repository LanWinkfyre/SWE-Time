# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Linux][Docs] Troubleshoot MCP Servers omits shared logs guidance from Hermes and Deep Agents variants

## Description

The published Troubleshoot MCP Servers guidance is inconsistent across the OpenClaw, Hermes, and Deep Agents documentation variants. The OpenClaw variant documents the logs command and OpenShell audit guidance, but the Hermes and Deep Agents variants omit the equivalent shared troubleshooting guidance even though the runtime command works for all three CLIs.

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
OpenClaw:      Available through the created sandbox workflow
```

## Steps to Reproduce

1. Open the published Troubleshoot MCP Servers pages for OpenClaw, Hermes, and Deep Agents.
2. Search each variant for the logs command guidance, including `logs --tail`.
3. Search each variant for the guidance that the logs output includes gateway and OpenShell audit information.
4. On a v0.0.119 Linux host, create one OpenClaw sandbox, one Hermes sandbox, and one Deep Agents sandbox.
5. Run the equivalent logs command against each sandbox.

## Expected Result

All three published variants should include the shared troubleshooting guidance for collecting logs and understanding gateway plus OpenShell audit evidence, because the equivalent command is supported across all three CLIs.

## Actual Result

The OpenClaw variant includes `logs --tail` guidance and OpenShell audit context. The Hermes and Deep Agents variants do not include the equivalent `logs --tail` guidance or the same warning about gateway and OpenShell audit evidence.

Runtime sanity showed that the command surface itself works across the three product variants, so the failure is a documentation variant omission rather than a product command failure.

## Logs

```text
OpenClaw logs command: exit code 0, returned gateway log output.
Hermes logs command: exit code 0, returned gateway and OpenShell audit output.
Deep Agents logs command: exit code 0, returned gateway and OpenShell audit output.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d35b4dfc2edbd7aa0ab4e5bc8771fbdbc3586536`.  There
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
{"case_id": "NVIDIA_NemoClaw__11175__d35b4df",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
