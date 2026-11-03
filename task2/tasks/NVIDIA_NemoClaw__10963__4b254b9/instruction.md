# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e: Hermes managed restart rejects required Hermes path variables

## Investigation Summary

- Four targets failed on candidate `3076188279c0ea657ec77aeeabebf1f82061eaaf`: [MCP bridge](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568882510), [Hermes E2E](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568882766), [Security: Hermes](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568886689), and [Hermes channels stop/start](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568886622).
- The exact cluster repeated on later main candidate `eb3fa2e5097389d7dd8e2643552788ff16d8f14a`: [MCP](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678904324), [Hermes E2E](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678904664), [Security](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678908612), and [channels](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678908280).
- Exact failures report `SECRET_BOUNDARY_REFUSED` for `HERMES_LAZY_INSTALL_TARGET`, `HERMES_HOME`, and `HERMES_BUNDLED_PLUGINS`.
- The restart validator hardened by [PR #10722](https://github.com/NVIDIA/NemoClaw/pull/10722) requires those paths, while the managed restart environment does not consistently supply the same canonical values.

## Description

Managed Hermes restart paths reject the environment constructed by NemoClaw itself. Operations that require a restart—MCP attachment, security validation, normal Hermes E2E, and channel lifecycle—therefore fail even though their initiating mutation succeeds.

Expected: every managed restart entry point supplies the same validated Hermes path contract as initial startup.

Actual: restart self-rejects at the secret-boundary validator.

## Reproduction Steps

1. Check out either candidate SHA above.
2. Run any linked Hermes E2E target that performs a managed gateway restart.
3. Observe `SECRET_BOUNDARY_REFUSED` or the wrapper error that the managed gateway restart did not complete.

## Environment

- GitHub Actions Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)
- Reproduced on two main candidates

## Debug Output

```text
SECRET_BOUNDARY_REFUSED
violations: HERMES_LAZY_INSTALL_TARGET, HERMES_HOME, HERMES_BUNDLED_PLUGINS
```

## Acceptance Criteria

- All managed restart entry points inject canonical values for the three required Hermes path variables.
- Negative secret-boundary tests continue to reject genuinely unsafe paths.
- All four affected targets pass on the same candidate in a full-suite run.


## Resolution

- [PR #11071 — fix(hermes): preserve sandbox lazy install target](https://github.com/NVIDIA/NemoClaw/pull/11071) merged on 2026-09-04 and closed this issue.
- The exact-candidate [E2E run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) tested commit 0ddc3ea52efe8a5d63099b92f43cbe0a43c88a01.
- Hermes E2E passed. The Hermes MCP gateway restart and corrected strict/compatibility integrity check passed before a later stored-provider credential failure now tracked by #11081.
- Hermes channel lifecycle and Hermes security also progressed past SECRET_BOUNDARY_REFUSED. Their later failures are tracked by #10971 and #11082.
- The original three-path-variable refusal is absent from the exact-candidate evidence. Full-suite restoration remains tracked by #10979.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4b254b9bef3e0ba745af4859fc65700742f5317e`.  There
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
{"case_id": "NVIDIA_NemoClaw__10963__4b254b9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
