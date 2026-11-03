# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
`health.maxUnitSize` never reaches the `unit_size` score penalty — the very-high-risk bin stays hardcoded at 60 LOC

### Summary

`health.maxUnitSize` (added in #1731) changes which functions are reported as large, but it does not change the `unit_size` penalty in `health_score`. The score's size bins (`1-15 / 16-30 / 31-60 / >60 LOC`) keep using a hardcoded 60, so a project that has deliberately set a different ceiling is still scored against fallow's default.

The observable result is confusing: raising the threshold empties the findings list while the deduction stays at exactly the same value.

### Reproduction

fallow 3.11.0, Next.js/TypeScript project, 631 functions analyzed, size profile `78% low · 14% medium · 6% high · 3% very high`. Only `health.maxUnitSize` varies between runs; everything else is identical.

| `health.maxUnitSize` | large functions listed | `health_score` | `penalties.unit_size` |
| ---: | ---: | ---: | ---: |
| 60 (default) | 19 | 76.3 | 10.0 |
| 100 | 10 | 76.3 | 10.0 |
| 120 | 9 | 76.3 | 10.0 |
| 150 | 5 | 76.3 | 10.0 |
| 200 | 2 | 76.3 | 10.0 |
| 250 | 1 | 76.3 | 10.0 |
| 300 | 0 | 76.3 | 10.0 |

The listing tracks the configured ceiling precisely — every step matches the sorted `line_count` inventory. The penalty does not move at all, and it is pinned at its cap.

The same decoupling applies to the other three thresholds. With `maxCyclomatic: 3`, complexity findings go from 21 to 79 while `penalties.complexity` stays 0.0 and the score stays 76.3. `unit_size` is the case where it is actually visible, because that penalty is non-zero and saturated.

For contrast, `health.ignore` *does* move the score (documented as "drops them from the score too"): removing one component directory took the score from 76.3 to 75.6. So the coarse lever — dropping files from the corpus — already lets a project shift its own score, while the precise lever — declaring the size at which a function counts as oversized — does not.

### Why the hardcoded 60 misfires

The bins look calibrated on imperative code. Applied to JSX/TSX they measure markup length rather than complexity: a component that renders a form is 120 lines with no branching, which is not a maintainability liability.

In the project above, 19 functions land in the very-high-risk bin. Three of them exceed the project's own ESLint ceiling (`max-lines-per-function: 150`). The other sixteen are flagged purely because the bin edge is 60 — an 84% divergence from the project's declared standard, and the largest offenders all carry an explicit `-- markup, not control flow` suppression at the call site.

A project that has thought about its ceiling and written it down has more information about its own code than a global default does.

### Proposed change

Let the very-high-risk bin edge in `crates/engine/src/vital_signs.rs` follow `config.health.max_unit_size` instead of the hardcoded 60.

- **No behavior change by default.** `maxUnitSize` already defaults to 60, so any project that has not set it scores exactly as it does today.
- **Continues the existing line.** #1731 made the ceiling configurable (list-only by design), #1750 surfaced it in the summary so the "Large functions" header could reflect the configured value rather than a static 60. The penalty is the remaining place where the default still wins over the configuration.
- **Threshold plumbing already exists.** `HealthSummary.max_unit_size_threshold` (#1750) carries the effective value.

If cross-project comparability of the grade is a concern, an explicit opt-in would address it without keeping the current asymmetry — e.g. `health.scoreUsesConfiguredThresholds: false` by default, plus a marker in the JSON output recording which basis a score was computed on. That seems preferable to the present situation, where the corpus is configurable but the yardstick is not.

### Fallback if the behavior is intentional

If the decoupling is deliberate, the documentation does not say so anywhere. The config-schema text reads "Raise thresholds to relax which functions are flagged" and, for `ignore`, "drops them from the score too" — which invites the inference that the thresholds affect the score as well. A sentence stating that `maxCyclomatic` / `maxCognitive` / `maxCrap` / `maxUnitSize` only govern findings and never `health_score`, plus a hint in the output when a non-default threshold sits next to a non-zero penalty, would have saved this investigation.

### Environment

- fallow 3.11.0 (darwin-arm64)
- Command: `fallow health --score --hotspots [--format json]`
- Config: `.fallowrc.jsonc`, only `health.maxUnitSize` varied between runs
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d00354b85399a5908d45f38bb890877c78e5375b`.  There
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
{"case_id": "fallow_rs_fallow__2116__d00354b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
