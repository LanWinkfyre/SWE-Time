# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][Sandbox] nemoclaw exec and status resolve sandbox against wrong gateway context in multi-gateway setup

## Description

In a two-gateway NemoClaw setup, `nemoclaw exec` and `nemoclaw status` intermittently route to the wrong gateway context, reporting "Sandbox does not exist" even though `nemoclaw list` shows the sandbox as registered. The same command succeeds on the first call and fails on the second with no state change between calls.

Platform scope: Reproduced on DGX Spark and Jetson Thor; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No.

## Environment

```text
Device:        Jetson Thor (aarch64) / DGX Spark (aarch64)
OS:            Linux 6.8.12-1021-tegra (Jetson) / DGX Spark Linux
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker Engine 29.6.2
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.120
OpenClaw:      v2026.7.1
```

## Steps to Reproduce

Pre-condition: a host that can run two NemoClaw gateway instances simultaneously.

1. Choose two non-conflicting gateway ports A and B.
2. Set `NEMOCLAW_GATEWAY_PORT={A}`, onboard sandbox `owner-a`, write a marker:
   ```bash
   nemoclaw owner-a exec -- sh -lc 'printf owner-a > /sandbox/workspace/gateway-owner.txt'
   ```
3. Set `NEMOCLAW_GATEWAY_PORT={B}`, onboard sandbox `owner-b`, write a different marker:
   ```bash
   nemoclaw owner-b exec -- sh -lc 'printf owner-b > /sandbox/workspace/gateway-owner.txt'
   ```
4. With the shell still pointing at gateway B, run:
   ```bash
   nemoclaw owner-a exec -- cat /sandbox/workspace/gateway-owner.txt
   ```
5. Immediately run the same command again (no state change):
   ```bash
   nemoclaw owner-a exec -- cat /sandbox/workspace/gateway-owner.txt
   ```
6. Run: `nemoclaw list --json`

## Expected Result

Steps 4 and 5: both calls exit 0 and route to the sandbox's recorded owning gateway (A), returning the correct marker regardless of the current shell's `NEMOCLAW_GATEWAY_PORT` value. The NemoClaw documentation states that a named sandbox's recorded owner should override the shell's current gateway selection.

Step 6: both sandboxes appear in the list.

## Actual Result

Step 4: First call succeeds — "Active gateway set to 'nemoclaw-8245'" and exits 0.

Step 5: Immediately after, the identical command fails:

```text
Sandbox 'owner-a' does not exist.
Did you mean: nemoclaw owner-b exec?
Registered sandboxes: owner-b
Run 'nemoclaw list' to see all sandboxes.
```

Step 6: `nemoclaw list --json` shows both sandboxes registered (owner-a and owner-b both present, `defaultSandbox = "owner-b"`).

Additional cross-contamination signal: on DGX Spark, `nemoclaw healthy-b exec` returned "Sandbox 'failure-a' does not exist" — exec on one sandbox returned an error referencing a completely different sandbox, confirming gateway context cross-contamination between calls.

The sandbox IS registered in NemoClaw state; exec cannot consistently resolve it on subsequent calls.

## Logs

Two consecutive exec calls for owner-b (Jetson, v0.0.120):

```text
[run] nemoclaw owner-b exec -- cat /sandbox/workspace/gateway-owner.txt
  Active gateway set to 'nemoclaw-8245'
  [exit 0 - SUCCESS]

[run] nemoclaw owner-b exec -- cat /sandbox/workspace/gateway-owner.txt
  Sandbox 'owner-b' does not exist.
  Did you mean: nemoclaw owner-a exec?
  Registered sandboxes: owner-a
  Run 'nemoclaw list' to see all sandboxes.
  [exit 1 - FAIL]

[run] nemoclaw list --json
  "defaultSandbox": "owner-b"
  "sandboxes": [{"name": "owner-b", ...}]

Reproduced across 4 independent CI runs on Jetson (2x) and DGX Spark (2x).
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f267027b9d3d3ce570267a43c118f32c9f25fdaf`.  There
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
{"case_id": "NVIDIA_NemoClaw__11410__f267027",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
