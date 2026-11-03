# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Preserve Portable startup failure evidence and distinguish saved phase from live health

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

Portable startup can fail with only a generic OpenShell status code. The standard debug command refuses a Portable authority candidate, and status can report retained lifecycle phase without observing live health.

At `e9cf24220532e33e704298632d9006b30254efdd`, a nonzero start discarded a harmless stderr canary. Timing reported `containerAction=started` despite failure. Public debug exited before collecting diagnostics.

## Reproduction

Inject a nonzero OpenShell start with a harmless diagnostic message. Compare public output and timing with the child result. Run public debug against an isolated Portable authority fixture. Query retained active authority while runtime health is unavailable.

## Acceptance

- Preserve useful, sanitized startup failure details and exit status.
- Record attempted and confirmed startup outcomes accurately.
- Label retained lifecycle phase separately from observed runtime or agent health.
- Define a supported diagnostic path for Portable failures within the accepted lifecycle scope.
- Test secret redaction and authority isolation before collecting diagnostic output.
- Preserve useful diagnostics when runtime services are unavailable.

Coordinate any newly supported debug behavior with repository scope requirements. Do not enable unrelated unsupported mutations or collect raw private receipts and environment data.


## Recorded evidence

The compiled debug command exited 1 before collection for an isolated Portable authority fixture. A harmless stderr canary was absent from the nonzero-start error; the timing result still recorded containerAction=started.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/onboard/experimental/hermes-portable-lifecycle.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/onboard/experimental/hermes-portable-lifecycle.ts)
- [Behavior owner: `src/lib/onboard/experimental/portable-agent-lifecycle.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/onboard/experimental/portable-agent-lifecycle.ts)

## Related work

Related #11248 documented lost primary startup causes. This issue records the remaining nonzero-start, diagnostic collection, and health-reporting behavior at the reviewed baseline.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ebb5e7555550cd43ea8de3e2bf6730f1534a0bf2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11651__ebb5e75",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
