# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
boundaries: optional calls, effects, and layer-coverage policy sections (boundary v2)

## Motivation

Boundary checks today are import-edge zone rules with presets and auto-discovered zones. That is the right zero-config default for JS/TS. The precision gap is that there is no banned-call policy, no effect-based policy, and no requirement that every file be assigned to a zone.

## Proposed (additive, opt-in, presets unchanged)

- `boundaries.calls.forbidden`: ban specific callees from a zone (e.g. `child_process.*` from `domain`, `console.*` from `domain`). Callee matching reuses the segment-aware patterns already used by the security catalogue.
- `boundaries.effects.allowed`: per-zone allowed effect classes. Depends on the internal effect classification (#1143).
- `boundaries.coverage.requireAllFiles` + `allowUnmatched`: flag files matched by no zone (catch unzoned files instead of silently treating them as unrestricted).

Example:

```jsonc
{
  "boundaries": {
    "zones": [],
    "rules": [],
    "calls": { "forbidden": [{ "from": "domain", "callee": "child_process.*" }] },
    "effects": { "allowed": [{ "zone": "domain", "effects": ["pure", "read", "unknown"] }] },
    "coverage": { "requireAllFiles": true, "allowUnmatched": ["src/generated/**"] }
  }
}
```

## Implementation note (important)

Land this in the live detector `fallow_cli::programmatic::detect_boundary_violations` (`crates/cli/src/programmatic.rs`), NOT in `crates/core/src/analyze/boundary.rs`, which is `#[deprecated(since = "2.76.0")]` per ADR-008 and points at the programmatic replacement.

This is a config-writer plus config-schema change, so it needs a config-focused review pass before merge.

## Acceptance

- `calls` and `coverage` sections work without the effect layer and ship first.
- `effects` section gated on #1143.
- Config schema and TS contracts regenerated; presets and existing zone rules unchanged.

Relates to: #1143 (effects section dependency).

Size: L.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `447094fdf27a3518060479d411c53dac6ce6982f`.  There
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
{"case_id": "fallow_rs_fallow__1147__447094f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
