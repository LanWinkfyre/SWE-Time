# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
upload-inventory: emit per-function complexity and caller edges (inventory blob v3)

The cloud's runtime-context `importance` and `blast_radius` rows are now emitted even when optional dimensions are missing, and in production every row has `caller_count: null`, `caller_count_weighted_by_traffic: null` and, for the rows that come from inventory backfill, `cyclomatic: null`. The cloud cannot compute those: they have to come from the inventory the CLI uploads (`fallow coverage upload-inventory`), whose blob is still `version: 1` and carries neither per-function complexity nor caller edges (`InventoryFunction` in the upload path).

### What to do

1. Extend the inventory blob to a `version: 3` shape that adds, per function, `cyclomatic` and `cognitive` from the health pass, and a compact `callerEdges` list (caller stable_id, callee stable_id) from the call graph the CLI already builds for `--blast-radius`. Keep `version: 1` readable and gate the new fields on the version so older clouds ignore them.
2. Size guard: cap edges per function and report the cap in the blob header so the cloud can say when a fan-in was truncated.
3. Document the new fields in the protocol crate (`fallow-cov-protocol`) and bump its version accordingly; the cloud reads them behind its existing `BLAST_RADIUS_CALLERS` flag.
4. Tests: a fixture project with a known call graph round-trips through the blob with the expected edge list and complexity numbers.

### Acceptance

- After an inventory upload from the new CLI, the cloud's runtime-context for that repo carries non-null `cyclomatic` on backfilled rows and non-null `caller_count` on functions that have callers.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `69d8d818a9d6b094545dae2f5c476cb0870feaa3`.  There
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
{"case_id": "fallow_rs_fallow__2607__69d8d81",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
