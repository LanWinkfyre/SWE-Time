# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
api: type-aware still requests the api-surface capability when private-type-leaks is off

Follow-up to #2170. The CLI no longer forces `private-type-leaks` on under type-aware, but the programmatic path (Node API, MCP, LSP) still derives `include_api_surface = include_all || filters.private_type_leaks` in `crates/api/src/type_aware/mod.rs` (both call sites), so a consumer with the rule explicitly off and no other filters active still requests the `ApiSurface` semantic capability from the sidecar. Findings are correctly suppressed downstream, so this is a wasted capability request (extra sidecar work), not wrong output.

Fix: thread the resolved rule severity into the capability derivation so `ApiSurface` is only requested when the rule is active. Surfaced during the v3.15.0 pre-ship review of the #2170 fix; verified on current main.
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
{"case_id": "fallow_rs_fallow__2218__9572854",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
