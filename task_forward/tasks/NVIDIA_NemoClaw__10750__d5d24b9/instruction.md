# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Agent&Skills] mcp restart reports success on a managed MCP provider with no valid credential

## Description

`mcp restart` on a managed MCP provider that has never resolved a valid credential exits 0 and prints a success message, instead of reporting that the provider is unavailable. A separate `mcp status --json` call immediately afterward correctly shows the provider as unhealthy, so the true state is discoverable elsewhere — the restart command's own exit code and message just do not reflect it.

Platform scope: Reproduced on Ubuntu 26.04 x86_64; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        x86_64 server (VM instance)
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Node.js:       v22.23.1
npm:           10.9.8
Docker:        29.6.1
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. Onboard any sandbox and add a managed MCP server without ever supplying a valid credential for it, e.g.:
   ```bash
   nemoclaw {sandbox} mcp add github --url https://api.githubcopilot.com/mcp/ --env GITHUB_MCP_TOKEN
   ```
   with only a placeholder/invalid value in `GITHUB_MCP_TOKEN` at add time, then unset the variable and never run a successful `mcp restart` on it.
2. Confirm the credential variable is unset host-side:
   ```bash
   test -z "${GITHUB_MCP_TOKEN:-}"; echo EXITCODE:$?
   ```
3. Run:
   ```bash
   nemoclaw {sandbox} mcp restart github; echo EXITCODE:$?
   ```
4. Immediately run:
   ```bash
   nemoclaw {sandbox} mcp status github --json
   ```

## Expected Result

Step 3 exits non-zero and identifies that the provider is unavailable / no valid credential is attached — it should not report success.

## Actual Result

Step 2:
```text
EXITCODE:0
```

Step 3:
```text
  Policy version 6 submitted
  Policy version 6 loaded (active version: 6)
  Applied preset: mcp-bridge-github
  Refreshed MCP server 'github'.
EXITCODE:0
```

Step 4 (run immediately after, same provider):
```json
{
  ...
  "provider": {
    "registryPresent": true,
    "attached": true,
    "credentialReady": true,
    "credentialResolution": {
      "ok": null,
      "detail": "probe skipped: the managed agent adapter does not match the current credential revision"
    }
  },
  "policy": {
    "name": "mcp-bridge-github",
    "registryPresent": true,
    "gatewayPresent": null
  },
  "adapter": {
    "registered": false,
    "detail": "mismatch"
  }
}
```

Step 3's own exit code and message ("Refreshed MCP server 'github'.") give no indication that step 4, run seconds later on the exact same provider, reports it as unhealthy with credential resolution unresolved.

## Logs

Not captured (terminal output above is the complete evidence for this defect; no additional gateway/container log was collected for this specific finding).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d5d24b9f97e223076ecdcb5f143a5a100da177dc`.  There
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
{"case_id": "NVIDIA_NemoClaw__10750__d5d24b9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
