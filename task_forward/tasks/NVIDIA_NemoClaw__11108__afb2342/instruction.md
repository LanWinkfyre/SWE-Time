# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Hermes lifecycle supervision must not gate relaunch on Hermes-owned mutable configuration

## Problem

NemoClaw lifecycle supervision treats the complete Hermes `config.yaml` and `.env` snapshot as relaunch authorization.
Hermes owns mutable configuration and persists normal runtime decisions there.
A valid Hermes mutation can therefore become a config-hash or MCP-integrity refusal.
The supervisor can then stop relaunch and require a sandbox rebuild even when Hermes is behaving normally.

This couples process supervision to agent configuration ownership.
The OpenShell-managed topology cannot establish configuration provenance because the supervisor, gateway, and agent share one UID.
The direct-root topology has a root-owned hash, but applying it to the complete mutable Hermes config prevents Hermes-owned changes from surviving lifecycle operations.

## Maintainer Decision

**Decision: Accept.**

- **Reason:** NemoClaw must have no opinion about valid config changes that Hermes invokes inside its sandbox.
- **Placement:** Keep process identity, health, crash-loop, path-safety, and secret-boundary controls in the supervisor. Move managed MCP reconciliation to the host command that owns that managed operation. Remove complete-config and managed-MCP equality as relaunch authorization conditions.
- **Accountable maintainer:** `@ericksoa`.
- **Validation plan:** Focused guard and supervisor tests must cover Hermes config adoption, host-side managed MCP mismatch reporting, secret refusal, path/race refusal, and process crash-loop quarantine.

## Desired Behavior

- A valid Hermes config change does not prevent startup, restart, recovery, or automatic respawn.
- NemoClaw validates paths and the credential boundary before it records the mutable config snapshot used by one restart.
- The current Hermes MCP config becomes the pending restart intent and becomes applied only after gateway health passes.
- A stale or incomplete host-managed MCP transaction cannot veto Hermes startup. The host command that owns that transaction can report a registry mismatch after Hermes is healthy.
- NemoClaw does not overwrite mutable Hermes config or require rebuild solely because its complete-file hash or MCP projection changed.
- Invalid Hermes configuration can fail Hermes startup and consume the existing crash budget. NemoClaw reports that launch failure without describing the config as unauthorized.

## Acceptance Criteria

- [ ] Valid Hermes config changes are adopted in both managed and direct-root lifecycle paths.
- [ ] The current MCP projection becomes pending and is committed only after gateway health.
- [ ] Stale managed MCP intent does not quarantine or stop Hermes.
- [ ] A host-managed MCP operation still detects and reports a registry mismatch without stopping a healthy gateway.
- [ ] Raw secret-shaped `.env` content remains denied and redacted.
- [ ] Unsafe paths and raced snapshots remain denied.
- [ ] Exact-process restart checks, health checks, auxiliary repair, and process crash-loop quarantine remain unchanged.
- [ ] Documentation describes Hermes config as mutable and limits integrity claims to restart snapshots and host-managed transactions.

## Related Work

- #10494 reports runtime self-writes that arm a delayed quarantine.
- #8649 reports the resulting restart and recovery failure family.
- #10696 removed core immutability and assigned optional immutability to composable blueprints.
- #5874 introduced the current supervisor.
- #6261 introduced managed MCP intended/applied state.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `afb2342666e0fa6b2dbaf23f1e194283b4787363`.  There
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
{"case_id": "NVIDIA_NemoClaw__11108__afb2342",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
