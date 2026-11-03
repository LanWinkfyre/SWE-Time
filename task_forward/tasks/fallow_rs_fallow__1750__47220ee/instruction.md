# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add maxUnitSize to the health summary (max_unit_size_threshold)

### Summary

`HealthSummary` (the `summary` block on `fallow health --format json`) carries `maxCyclomaticThreshold`, `maxCognitiveThreshold`, and `maxCrapThreshold`, but not a unit-size sibling. When `health.maxUnitSize` became configurable (#1731), that left a parity gap: a consumer reading the health summary to learn "what thresholds is this run using" now sees three of the four.

### Proposed change

Add `max_unit_size_threshold: u32` to `HealthSummary`, populated from `config.health.max_unit_size` at the summary builder, so the effective global unit-size ceiling is surfaced alongside the other three.

Two follow-on benefits:

- The two hand-rolled effective-threshold fallbacks in the human and markdown complexity-finding renderers currently fill the now-required `HealthEffectiveThresholds.max_unit_size` with the hardcoded default (60) rather than the configured global. Today that field is inert (it is not rendered on complexity findings), but a summary field would let those fallbacks use the real value if it is ever read.
- It would let the "Large functions" section header reflect the configured global instead of a static "60" when `health.maxUnitSize` is raised project-wide.

### Cost / why it was deferred from #1731

`HealthSummary` has 20+ construction sites (the real builder plus many full test literals across snapshot, codeclimate, badge, and human-report tests) and a `Default` impl, and it is part of the published output contract (schema + TS codegen + snapshots regen). #1731 was scoped as a minimal, list-only change, so adding an always-present summary field for a currently non-rendered value was left as this separable follow-up.

### Notes

Additive-required field on the summary; matches the existing `max*Threshold` siblings. No behavior change to the unit-size check itself.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `47220ee76899388cf5bc1298b083c644a5067495`.  There
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
{"case_id": "fallow_rs_fallow__1750__47220ee",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
