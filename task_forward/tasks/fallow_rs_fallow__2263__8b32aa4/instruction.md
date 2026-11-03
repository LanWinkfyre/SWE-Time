# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
graph: ambiguous star exports drop reference credit from every contributing origin

When a name is supplied by two different `export *` sources, `attach_direct_export_references` requires a `Unique` resolution and skips the name entirely:

```rust
// crates/graph/src/graph/narrowing.rs:593
let super::EffectiveExportResolution::Unique(binding) =
    effective_exports.resolve(target_module.file_id, imported_name, namespace)
else {
    continue;
};
```

An `Ambiguous` resolution therefore credits nothing, and every declaration that contributed to the collision ends up with zero references from that import site. Both `left.ts` and `right.ts` in the collision look unused even though a consumer imports the name from the barrel.

**Why this is the awkward case**

Strictly, the ambiguous export does not exist per the spec, so the import is broken code and no crediting is "correct". But fallow reports on real repositories where this pattern is usually an accident in one barrel, and the current behavior converts one barrel mistake into unused-export findings against two innocent source files. That is the false-positive direction, which the detector contract elsewhere treats as the expensive one.

**Options worth weighing**

1. Credit every contributing origin on `Ambiguous` (conservative, no new findings, hides the collision).
2. Keep the current skip but emit a distinct diagnostic for the collision so the resulting unused-export findings are explainable rather than mysterious.
3. Suppress unused-export findings for declarations that participate in a known ambiguous collision, without crediting them as used.

Option 2 or 3 keeps the accuracy story honest; option 1 is the cheapest. `contributes_through` already handles the ambiguous case for a related path, so the graph layer has the shape needed for either.

Found while reviewing #2210. Related: #2262 (the same state is invisible in `fallow trace`).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8b32aa4f6a285d1ae6897986f99dde834ecb7579`.  There
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
{"case_id": "fallow_rs_fallow__2263__8b32aa4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
