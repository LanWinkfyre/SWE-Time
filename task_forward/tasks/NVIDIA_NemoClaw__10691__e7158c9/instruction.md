# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Adopt OpenShell ForwardTcp for NemoClaw-managed host forwards

Parent: #9802

Related: #9808, #7174, #10385, #10496, #10640, NVIDIA/OpenShell#874, NVIDIA/OpenShell#1029, and prior draft PR #4329.

## Outcome

Replace NemoClaw-owned SSH host forwards with OpenShell's direct raw `ForwardTcp` path through `openshell forward service`.

NemoClaw launches the foreground OpenShell command as a detached child and waits for the requested local port. OpenShell owns the forward lifetime. NemoClaw stores no forward receipt, PID, process identity, supervisor state, or migration marker.

## Scope

- Launch explicit `openshell --gateway <name> --workspace default forward service ...` commands.
- Refuse a requested local port that is already occupied. Do not adopt or signal its process.
- Confirm that the requested port becomes reachable before reporting success.
- Let OpenShell terminate the forward when the sandbox or gateway becomes unavailable.
- Let normal recovery launch the forward again.
- Make stop, destroy, and rebuild wait for ports to release after the sandbox becomes unavailable.
- Retire only legacy `(gateway, sandbox, port)` entries declared by NemoClaw.
- Remove the legacy forward starter, watcher, orphan reaper, stale-listener reaper, process scanner, and uninstall forward sweeps.
- Keep the installer-only migration that stops an exact known legacy watcher before invoking normal recovery.

## Security and failure behavior

- Target the recorded gateway and sandbox explicitly.
- Exclude ambient endpoint and credential overrides from the OpenShell child environment.
- Do not persist credentials or process state.
- Do not inspect, adopt, or signal a ForwardTcp process.
- Fail when a foreign listener already occupies the requested port.
- Do not retry through SSH or another transport.

## Acceptance criteria

- OpenClaw dashboard HTTP, bearer-protected requests, and WebSocket traffic work through `forward service`.
- Hermes dashboard and bearer-protected API requests work through `forward service`.
- Teams webhook authorization and the shared Google Chat surface remain intact.
- Stop, destroy, rebuild, and gateway loss release their host ports through OpenShell's natural lifecycle.
- Recovery relaunches missing forwards.
- Known NemoClaw legacy forwards migrate; undeclared user forwards remain untouched.
- Loopback, WSL, explicit `0.0.0.0`, headless SSH-tunnel, Linux, and macOS behavior remain covered.
- The final production change is smaller than the subsystem it removes.

## Out of scope

- `openshell service expose`
- Direct TypeScript SDK packaging
- Manifest schema redesign
- Dynamic local ports
- Decoupling host ports from in-sandbox ports
- Public `nemoclaw forward` commands
- Reboot persistence or a new service-manager contract
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e7158c9908cadae49271666aede8c5ce726a79d9`.  There
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
{"case_id": "NVIDIA_NemoClaw__10691__e7158c9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
