# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit: cache GC diagnostics and a manual prune command

Follow-up to #2169. The base-snapshot cache GC now reclaims abandoned cross-repo entries, but it runs silently: there is no way to see what it considered, skipped (live owner), or reclaimed, and no way to trigger a cleanup without running an audit.

Proposed:
- debug-level GC diagnostics (candidate, decision, reason) behind the existing verbosity/env conventions,
- a manual cache-prune command (or flag) that runs the same reclaim logic on demand and prints what it removed,
- from the same review: replace the `Path::exists()` owner-liveness probe with a deliberate NotFound-only check so permission or mount errors do not read as a dead owner (both currently fail toward a cheap cache rebuild, which is safe but worth making explicit).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95728543e804a0e4a4a0ca9dd239f328c6adde4d`.  There
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
{"case_id": "fallow_rs_fallow__2221__9572854",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
