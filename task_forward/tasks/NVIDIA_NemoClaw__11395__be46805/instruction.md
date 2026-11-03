# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Install] uninstall refuses a gateway from an onboard interrupted before sandbox registration (regression of closed #10544)

## Description

`nemoclaw uninstall --yes` (scoped to a specific gateway port) refuses to clean up a gateway left behind by an onboard that was interrupted before a sandbox got registered, exiting 1 with "Refusing scoped gateway cleanup because its sandbox namespace cannot be proven." This is the exact symptom of #10544, which was closed as COMPLETED on 2026-08-29 — reproduced fresh today on v0.0.121, independently confirmed as the root cause of a real production annoyance: this same error blocked a manual full-host uninstall (`--all-gateway-ports`) being run live today on a separate DGX Spark host, where two sibling gateways hit this exact refusal and had to be removed by hand.

The refusal is self-perpetuating exactly as #10544 described: the gateway has no sandbox precisely because the onboard died before creating one, so the namespace check can never be satisfied for that gateway, and no uninstall variant (plain, `--all-gateway-ports`, with `NEMOCLAW_OPENSHELL_GATEWAY_STATE_DIR` override) clears it — the only way back to a clean host is deleting the state directory by hand.

Platform scope: Reproduced on Ubuntu 24.04 x86_64 (matches #10544's own platform scope, which also included DGX Spark aarch64).

> [!WARNING]
> Regression: #10544 was closed as fixed on 2026-08-29; this reproduces unchanged on v0.0.121 (released after that date). Recommend triage confirm whether #10544's fix actually shipped, was reverted, or never covered this exact code path.

## Environment

```text
Device:        Ubuntu 24.04 x86_64 host
OS:            Ubuntu 24.04
Architecture:  x86_64
NemoClaw:      v0.0.121
```

## Steps to Reproduce

1. Start an onboard on a fresh gateway port and let it run only through preflight (before sandbox creation/registration), e.g.: `NEMOCLAW_GATEWAY_PORT=19041 timeout 30 nemoclaw onboard --agent openclaw --name a4-test --non-interactive --fresh --yes --yes-i-accept-third-party-software --no-gpu` — the short timeout kills it mid-preflight, before any sandbox is registered.
2. Confirm the gateway state directory exists but no sandbox was registered: `ls ~/.nemoclaw/gateways/19041` (exists) and `nemoclaw list` (no sandboxes).
3. Run `NEMOCLAW_GATEWAY_PORT=19041 nemoclaw uninstall --yes`; capture output and exit code.

## Expected Result

Uninstall exits 0. Output does not contain a sandbox-namespace refusal error. The incomplete gateway state is removed rather than triggering an exit-1 abort, since there is provably no sandbox for this gateway to protect.

## Actual Result

Exit code 1.

```text
Refusing scoped gateway cleanup because its sandbox namespace cannot be proven.
If onboarding used a gateway state override, rerun with NEMOCLAW_OPENSHELL_GATEWAY_STATE_DIR=<absolute-path> set to its original resolved directory.
```

The gateway state directory (`~/.nemoclaw/gateways/19041`) remains on disk afterward; `nemoclaw uninstall --all-gateway-ports` also does not clear it.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `be46805b51b0d626466538e9f8fe56c8ad157549`.  There
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
{"case_id": "NVIDIA_NemoClaw__11395__be46805",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
