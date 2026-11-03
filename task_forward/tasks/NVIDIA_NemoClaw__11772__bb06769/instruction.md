# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Retire obsolete lifecycle recovery and E2E machinery

Part of #11255. Focused delivery slice of #11765. Begin after #11695 merges.

## Problem

Native-loopback qualification exposed live E2E coverage that still exercises NemoClaw-owned lifecycle and recovery behavior we intend to remove. In the exact-head #11695 run, the supported OpenShell stop/start path passed, while `gateway-guard-recovery` failed only in its later legacy `sleep infinity` container-replacement transaction. `sandbox-survival` failed before gateway restart because retained NemoClaw recovery records conflicted with current Docker identities. Those paths are validating obsolete machinery rather than the basic-onboarder architecture.

The authorization target also coupled its scope contract to a hosted agent turn: the required `operator.write` state settled successfully, but the job failed when the unrelated OpenClaw/inference turn timed out.

Evidence: https://github.com/NVIDIA/NemoClaw/actions/runs/34902351251 on #11695 head `7993b26a5dffb7980000b27af839532a5a5c0733`.

## Scope

- Delete the legacy keepalive/container-replacement branch from `gateway-guard-recovery` and remove production recovery helpers whose only remaining consumer is that branch.
- Refocus or retire `gateway-guard-recovery` so it covers only behavior NemoClaw still owns after onboarding.
- Replace NemoClaw retained-registry/recovery orchestration in `sandbox-survival` with OpenShell stop/start plus native agent readiness and state-survival assertions.
- Delete stale recovery records, immutable replacement-transaction state, rollback/handoff code, and fixtures that have no supported runtime consumer.
- Keep the scope-upgrade test focused on authorization. Do not make successful hosted inference the verdict for an already-proven scope transition unless that agent turn is itself the contract under test.
- Remove target-catalogue and workflow wiring for any live target that becomes empty.
- Do not build replacement lifecycle machinery.

## Acceptance criteria

- [ ] The legacy `sleep infinity` replacement transaction and its assertions are gone.
- [ ] OpenShell is the lifecycle actor for supported sandbox stop/start; native agents own their gateway and background processes.
- [ ] `sandbox-survival` begins from clean state without NemoClaw retained-recovery identity conflicts and verifies only supported ownership boundaries.
- [ ] Authorization evidence distinguishes scope settlement from workload/inference availability.
- [ ] Obsolete production helpers and fixtures are deleted, with the removed inventory and net line reduction recorded in the PR.
- [ ] Existing credential-placement, exact-sandbox targeting, containment, and negative-egress evidence remains strict.
- [ ] Deterministic tests cover remaining parsing, migration, and security boundaries; live E2E is reserved for actual OpenShell/native-runtime behavior.
- [ ] The PR records the E2E target/job reduction.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bb06769017135c7b16e9809c45afd9cf91bc6a76`.  There
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
{"case_id": "NVIDIA_NemoClaw__11772__bb06769",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
