# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
action: install or wire the fallow-type-aware sidecar for typeAware-enabled projects

Follow-up to the distribution gap reported in #2103. The GitHub Action installs only the standalone CLI binary, so projects with `typeAware.enabled` silently fell back to syntactic analysis before v3.11.0 and need manual `FALLOW_TYPE_AWARE_BIN` wiring now. Options: install `fallow-type-aware@<resolved version>` alongside the binary when the project config enables type-aware, or document the project-local-install wiring prominently in the Action docs. The exact-version match contract must hold either way.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9a3ae1440dc7bbd228306924083746c818837eb3`.  There
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
{"case_id": "fallow_rs_fallow__2107__9a3ae14",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
