# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Complete gateway lifecycle adapter migration after #9807 observation slice

Parent capability: #9807. Parent epic: #9802.

## Accepted scope

Decision: Accept. Rebecca Sliter authorized the observation-first delivery split and the narrower cleanup fallback in #9807.

Reason: Complete the gateway adapter migration while moving lifecycle operations and their coupled observations together.

Placement: Extend the typed OpenShell adapter established by #9807. Preserve existing NemoClaw ownership and recovery policy.

Accountable maintainer and implementation owner: @rsliter.

## Outcome

Route registration, selection, startup, shutdown, removal, destruction, and lifecycle-coupled health/reuse observations through the asynchronous gateway adapter.

Deferred consumers from the observation slice:

- Onboarding gateway registration, start, recovery, process lifecycle, reuse snapshots, health waits, and readiness production collection.
- Host-runtime and Docker-driver gateway readiness, service, and cutover flows.
- Snapshot gateway metadata health and selection.
- Destroy and uninstall gateway mutations and cleanup.
- Gateway selection and startup within named-gateway recovery; shared before/after observations migrate in Slice 1.
- Remaining raw gateway state helpers after their final lifecycle consumer migrates.

## Acceptance evidence

- Preserve explicit gateway identity, endpoint guards, ownership checks, lifecycle locks, and sibling-gateway isolation.
- Use legacy gateway destruction only when removal is explicitly unsupported and existing ownership rules permit it.
- Authentication, permission, timeout, transport, and other removal failures must not trigger legacy destruction.
- Re-read ownership and state after an ambiguous mutation; stop if safety cannot be verified.
- Preserve externally supervised gateway restrictions and credential redaction.
- No automatic mutation retries or cross-transport fallback.
- Migrated consumers use typed results without constructing argv or parsing CLI output.

## Validation plan

Typed-fake action tests; CLI command, error-mapping, targeting, timeout, and redaction tests; existing onboarding, ownership, process, destroy, and uninstall regressions; focused live evidence for changed external boundaries.

## Sequencing

Depends on observation and targeting PR #11330 for #9807. Keep #9807 open until both slices meet their acceptance criteria. Record final consumer dispositions in #9813.

## Exclusions

SDK/gRPC migration, dependency upgrades, authentication redesign, installation changes, sandbox create/delete (#9811), provider operations (#9806), and plugin migration (#9813).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f47724f29838fe08898993fad1c8c6b7fcb3e080`.  There
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
{"case_id": "NVIDIA_NemoClaw__11326__f47724f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
