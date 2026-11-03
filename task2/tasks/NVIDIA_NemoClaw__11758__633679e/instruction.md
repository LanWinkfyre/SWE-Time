# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
fix(onboard): preserve secret-boundary refusals through finalization

## Problem

Fresh Portable Hermes onboarding reports `PRIVILEGED_CONTROL_UNAVAILABLE` and “Secret-boundary check did not complete cleanly … Refusing recovery”, then prints “Deployment verified” / “Hermes is ready” and exits 0.

Observed during successful prompt and real-response runs on `a9db662a35eacdc22993271d34a097446a4c30d7` and `6c3837017d6c2811b457ddeffa813aeb832f1e83`. The marker means validation could not complete; it is not evidence that a secret was exposed. Relevant finalization code is unchanged on main `7892d143d282ab0ffb25b0cd1c7ddd228c0a8313`.

## Cause and detection gap

The onboarding finalization dependency awaits `checkAndRecoverSandboxProcesses` but discards its structured result through a `Promise<void>` interface. A returned secret-boundary refusal therefore does not prevent onboarding from advancing to later readiness checks and success. Tests of the recovery helper alone do not exercise this consumer boundary.

## Expected behavior and acceptance

- Preserve a secret-boundary refusal from process recovery through onboarding finalization, including the later post-verification recovery call.
- Do not report successful onboarding, deployment readiness or a successful handoff when the required boundary check refuses or cannot complete.
- Retain a resumable, explicit failure/incomplete state and a safe actionable diagnostic.
- Successful validated recovery continues normally. Cover raw-secret refusal, unavailable/missing validator/control, and success without leaking captured diagnostics.
- Add failing-before/passing-after regression evidence through the actual finalization dependency and state-machine consumer.

## Scope

Part of #11573. Separate from #11735. This fix propagates required validation outcomes; it must not disable the validator, treat unavailable privileged control as success, or claim to repair the underlying privileged-control discovery problem without separate evidence.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `633679ee17956c0035186eecc2dca7fea2d5d884`.  There
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
{"case_id": "NVIDIA_NemoClaw__11758__633679e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
