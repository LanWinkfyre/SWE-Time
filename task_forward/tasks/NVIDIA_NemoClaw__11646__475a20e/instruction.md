# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Reconcile saved sandbox phase with runtime state during Portable recovery

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

An inconsistent saved phase can prevent recovery or report a successful start while the container remains stopped.

At NemoClaw `e9cf24220532e33e704298632d9006b30254efdd`, isolated OpenShell 0.0.116 tests reproduced three failures:

- A real image configuration failure reached Error. A later start failed because the saved phase was not Stopped.
- A healthy container with an injected saved Error refused both start and exec.
- An exited container with an injected saved Ready reported successful start but remained exited. Exec exceeded the harness deadline.

Restoring the correct Stopped phase allowed start and exec. Separate NemoClaw tests show that an unhealthy workload in a running container receives health polling without workload relaunch.

These controls use a minimal Ubuntu workload and a disposable database. They establish the state mismatch behavior, not the cause of John's failure or Hermes recovery performance.

## Reproduction

Run the disposable OpenShell healthy control described below. Repeat with deliberately mismatched saved phases in that disposable runtime. Separately use an image without the required OCI user to reach Error naturally. Retain container state, saved phase, command output, and exit status for each run.

## Acceptance

- Reconcile saved phase, container state, and managed workload readiness before reporting success.
- Recover through the owning lifecycle API when recovery is supported. Preserve actionable failure evidence when it is not.
- Do not reset database phase or directly mutate an unqualified container as a repair.
- Preserve timeout rollback, identity checks, and retained user data.
- Repeat healthy stop/start, Error, Ready/exited, and unhealthy-workload controls against the fix.



## Recorded evidence

OpenShell 0.0.116: saved Error + running container refused start/exec; saved Ready + exited container returned start success while the container stayed exited. A correct Stopped control restarted and executed successfully.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/onboard/experimental/hermes-portable-lifecycle.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/onboard/experimental/hermes-portable-lifecycle.ts)

## Related work

Related historical reports #11248, #11302, and #8112 are closed. This issue tracks the reproduced saved-phase/runtime mismatch at the stated newer baseline; it does not reopen their distinct manifest migration or stop-settlement scopes.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `475a20e00db5984d026b70d0a01654a2822b6a7a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11646__475a20e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
