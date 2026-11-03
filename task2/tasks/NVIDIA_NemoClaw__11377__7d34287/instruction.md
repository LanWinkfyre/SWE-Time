# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][Policy&Network] mcp status reports no valid endpoint for a trusted-private-host MCP server

## Description

A managed MCP server registered against a trusted private (RFC1918) address via the documented `--trusted-private-host` flag adds successfully, but every subsequent tool-discovery check against that same server fails with a generic "no valid managed endpoint is available" message instead of listing its tools.

Platform scope: All Platforms -- reproduced on DGX Spark, but root cause is the MCP status/discovery re-validation path (trusted-private-host list not carried forward) with no platform/hardware dependency; expected to reproduce identically on any platform.
Regression: Unknown - earlier versions not tested this session. A related, previously-filed issue (#8746) investigated the same symptom class on an older OpenShell version and was closed in 2026-08 without a root cause being assigned - this may be the same long-standing defect.

## Environment

```text
Device:        DGX Spark
OS:            Ubuntu (aarch64)
Architecture:  aarch64
Node.js:       v22.22.1
npm:           10.9.4
Docker:        28.3.3 (build 980b856)
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.121
OpenClaw:      2026.7.1 (2d2ddc4)
```

## Steps to Reproduce

1. Stand up any HTTPS Streamable HTTP MCP server reachable at a private/RFC1918 address (e.g. a Docker bridge IP), advertising at least one tool.
2. Register it against a Ready sandbox using the documented trusted-private-host mechanism:
   ```bash
   nemoclaw {sandbox} mcp add {server} --url https://{private-ip}:{port}/mcp --env {KEY} --trusted-private-host {private-ip}
   ```
3. Confirm the add succeeded - the command's own output reports the provider attached, the policy applied, and `"trustedPrivateTarget": {"state": "match"}`.
4. Run:
   ```bash
   nemoclaw {sandbox} mcp status {server} --tools --json
   ```

## Expected Result

Tool discovery succeeds and returns the MCP server's advertised tools, since the server was just confirmed registered and trusted in step 3.

## Actual Result

Tool discovery always fails, immediately and consistently across repeated attempts, with:

```json
{
  "toolDiscovery": {
    "ok": false,
    "count": 0,
    "tools": [],
    "detail": "tool discovery skipped: no valid managed endpoint is available",
    "failedStage": "preflight",
    "failureClass": "precondition"
  }
}
```

The rest of the status output (provider attachment, credential readiness, policy presence, `trustedPrivateTarget.state`) all report healthy/matched - only tool discovery fails, with a message that gives no indication the private-host trust context is the actual problem.

## Logs

Not captured beyond the `--json` output shown above.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7d3428718f2591b2023ffe2bb72ed990e6856f81`.  There
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
{"case_id": "NVIDIA_NemoClaw__11377__7d34287",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
