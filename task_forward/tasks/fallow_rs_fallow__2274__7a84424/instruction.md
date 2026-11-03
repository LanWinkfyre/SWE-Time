# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Extend the star-collision suppression gate to the detectors that still abstain

The unused-export surface suppresses its own findings for names lost to an ambiguous `export *` collision (shipped in #2268). Three other surfaces still abstain on `Ambiguous` with no such gate, so the same barrel mistake can still produce a finding that names the wrong file. The unrendered-component header documents its carve-out verbatim:

> The remaining way this detector can flag a rendered component is UNDER-crediting on an ambiguous name. [...] the crediting walks abstain there, so a component reached only through the colliding name is credited by nobody and stays eligible. The finding then names the component while the fault is in the barrel.

**Sites**

1. `crates/core/src/analyze/unrendered_component.rs` — the crediting walks abstain on `Ambiguous`, while eligibility comes from the raw `re_exports` and does not abstain. A component rendered only through a colliding name is flagged as unrendered.
2. `crates/core/src/analyze/members/mod.rs:475` — the class-member walk returns an empty vec on `Ambiguous`, so members reached only through a colliding name lose their crediting.
3. `crates/graph/src/graph/mod.rs:1010` `unique_export_bindings` — excludes ambiguous exports by contract, which feeds the namespace and public-API lanes. Callers inherit the abstain without knowing it happened.
4. `crates/core/src/analyze/unprovided_inject.rs` — reaches the same `walk_re_export_origins` path through `resolve_key`.

**Shape**

`ModuleGraph::ambiguity_participants()` already exists and is what the unused-export gate consumes. Applying the same emission-point guard to each surface should be mechanical; the work is in deciding per detector whether suppression or something better fits, and in a fixture per surface proving the finding disappears while unrelated findings stay.

Worth checking while doing this: whether `unique_export_bindings` should keep silently dropping ambiguous names, or expose them so callers choose. Silent exclusion inside a shared accessor is how this spread in the first place.

Follow-up to #2263.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7a8442440410c9e3211ac28028fd415e8ee4e303`.  There
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
{"case_id": "fallow_rs_fallow__2274__7a84424",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
