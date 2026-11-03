# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
observeManagedGateway() hardcodes Docker CLI calls, breaking native Podman onboarding after #10900

## Summary

After #10900 (merged — fixed the host-prerequisite preflight to respect `NEMOCLAW_GATEWAY_RUNTIME=podman`), onboarding still fails one step later, at the gateway-reuse/readiness check. `observeManagedGateway()` in `src/lib/readiness/gateway-production.ts` is entirely Docker-specific — it imports exclusively from `../onboard/docker-driver-gateway-*` modules and does raw `spawnSync("docker", ["inspect", ...])` calls (e.g. lines 371, 375, 402), with no branching on the selected runtime. On a host without Docker installed — the exact target environment `NEMOCLAW_GATEWAY_RUNTIME=podman` is meant for — every one of these calls fails, and onboarding reports `gateway.reuse.ready`, `gateway.version.compatible`, and `gateway.port.uncontested` as unable to be confirmed.

## Steps to Reproduce

1. On a Linux host with rootless Podman and no Docker installed.
2. Install NemoClaw from `main` (post-#10900) with `NEMOCLAW_GATEWAY_RUNTIME=podman`.
3. Onboarding reaches `[1/8] Preflight checks` and fails. Reproduces on a fully fresh install with no prior NemoClaw/OpenShell state.

## Error Logs / Traceback

```
[1/8] Preflight checks
──────────────────────────────────────────────────
✗ System readiness could not confirm required capabilities: gateway.reuse.ready, gateway.version.compatible, gateway.port.uncontested.
Managed gateway observations could not be collected safely.

Onboarding did not finish. Resume from the step that failed with:
  nemoclaw onboard --resume --name <sandbox>
```

## Root Cause

`src/lib/readiness/gateway-production.ts`'s `observeManagedGateway()`:
- Imports only from `docker-driver-gateway-env`, `docker-driver-gateway-local-tls`, `docker-driver-gateway-port-listener`, `docker-driver-gateway-process-identity`, `docker-driver-gateway-runtime`, `docker-driver-gateway-service`.
- Calls `listenerHelpers.getDockerDriverGatewayPortListenerScan(...)` unconditionally.
- Shells out directly to `docker inspect` at lines 371, 375, and 402.

No Podman-equivalent path appears to exist for this specific readiness check yet, unlike the host-preflight fix in #10900.

## Environment

- Fedora 44, x86_64, rootless Podman 5.8.4, no Docker installed
- NemoClaw `main`, tested post-#10900 merge

## Related

Follows #10891 / #10900 — same native-Podman-activation effort, one layer deeper.
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
{"case_id": "NVIDIA_NemoClaw__10984__3e605bc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
