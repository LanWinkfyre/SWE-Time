# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
fix(onboard): extend Podman container discovery settlement after OpenShell Ready

## Summary

A newly created OpenShell sandbox can be reported Ready before its labeled Podman-backed container is visible to NemoClaw's privileged Docker control path. Hermes post-onboarding then exhausts the current 30-second managed-control settlement window with `PRIVILEGED_CONTROL_UNAVAILABLE`, even though the sandbox becomes healthy shortly afterward.

## Evidence

- Reproduced by Portable Build 346 with candidate `e6d435819bc7c4a5c07860665c5712173f6e47a9`.
- Sandbox creation, authenticated Hermes health, dashboard, and inference-route checks succeeded.
- The immediate privileged secret-boundary recovery returned only the exact sanitized `PRIVILEGED_CONTROL_UNAVAILABLE` startup marker.
- A later explicit probe found and reused the same healthy container; no Podman restart or container recreation was required.
- Forward recovery then could not establish the required host forwards, including port 8642, because onboarding had advanced past the unsettled privileged-control phase.

## Required behavior

1. Keep the happy path unchanged.
2. Treat only the exact, sanitized `PRIVILEGED_CONTROL_UNAVAILABLE` result as a transient startup observation.
3. Extend the bounded post-create settlement window enough for the observed OpenShell Ready-to-container-discovery handoff.
4. Continue to fail immediately on identity, integrity, malformed-output, ambiguous-container, or diagnostic-bearing failures.
5. Add regression coverage proving settlement can succeed after the former bound and that diagnostic-bearing failures remain terminal.
6. Run focused managed-startup/process-recovery tests and PR validation.

## Security constraints

- Do not accept process presence as proof of sandbox identity.
- Do not relax immutable container identity pinning.
- Do not retry diagnostics that contain anything beyond the exact approved startup marker.
- Do not emit credentials or unsanitized runtime output.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `78e502e58692d2711f00046f724f91ecca470bb4`.  There
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
{"case_id": "NVIDIA_NemoClaw__11107__78e502e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
