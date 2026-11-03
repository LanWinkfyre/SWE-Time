# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: add direct_callers and clone_siblings to refactoring-target evidence

## Motivation

`health --targets` ranks refactoring targets and attaches `TargetEvidence`, but the evidence is metric-composed rather than relation-explained. `TargetEvidence` (`crates/cli/src/health_types/targets.rs`) carries `unused_exports`, `complex_functions`, and `cycle_path` only. An agent cannot see "who calls this" or "what duplicates this" without separate calls.

## Proposed (cheap, data already available)

Add two evidence fields, both derivable from systems that already run:

- `direct_callers`: files / symbols that import or call the target (graph reverse-deps).
- `clone_siblings`: clone-group members touching the target (existing clone fingerprints).

## Deferred (tracked here for context, not in this slice)

These depend on the relation and effect substrate and should land after it:

- `blocking_effects` (side effects that block safe extraction) and `pure_regions` (extractable pure regions inside mixed-effect functions): depend on #1142 and #1143.
- `suggested_tests`, `transitive_callers`, `why_ranked`.

## Acceptance

- `direct_callers` and `clone_siblings` populated on target evidence in `--format json`, additive and `skip_serializing_if` empty.
- Typed in `output_health` / `health_types`, picked up by the TS codegen.
- Human output unchanged unless the fields are non-empty.

Relates to: #1142, #1143 (later proof objects).

Size: S/M.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `87e983e33813043ae1f0c3733d0ca86219daf399`.  There
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
{"case_id": "fallow_rs_fallow__1145__87e983e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
