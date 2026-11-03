# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Passing --coverage can lower a function's CRAP and let --max-crap pass

Handing fallow a coverage map can make `--max-crap` more permissive than running with no coverage data at all.

## Reproduction

A project with one arrow function carrying ten branches, in a file a test reaches, and a coverage map that contains the file but whose records cannot be attributed to that function (a stale map, a renamed function, a producer whose anchors fallow does not resolve).

```
fallow health --complexity --max-crap 30
  branchy  crap 31.6  coverage_source estimated  ->  finding, exit 1

fallow health --complexity --coverage coverage-final.json --max-crap 30
  branchy  crap 10.0  coverage_source estimated  ->  no finding, exit 0
```

Same code, same threshold. The run with real coverage data passes.

## Cause

Two paths disagree about what an unmatched function is worth. In `crates/engine/src/health/scoring.rs`, the unmatched branch of `crap_for_function` returns `cc` for a function in a test-reachable file, which is the CRAP of a fully covered function. The no-coverage-file path, `compute_crap_scores_estimated` in the same file, returns `crap_formula(cc, 40)` for the identical function. So a function that fails to match is scored as if it were fully covered, and only when a coverage map is present.

The same branch also emits a coverage tier without a percentage:

```json
{ "name": "branchy", "crap": 10.0, "coverage_tier": "partial", "coverage_pct": null, "coverage_source": "estimated" }
```

`coverage_tier: "partial"` is derived from an internal estimate constant while the percentage stays null, so a consumer reads "partly covered" for a function the map never measured.

## What needs deciding

The invariant is easy to state and hard to argue with: **adding a coverage map must never lower a function's CRAP unless the map attributes coverage to that function.** The open question is what the unmatched-but-test-reachable case should score under an Istanbul model. Reusing the 40 percent estimate keeps the two paths consistent and means they should share one estimator. Scoring it at zero cannot be gamed but would flood dependency-injection heavy codebases, where whole modules are never imported by a unit test, with findings on the first run.

Second decision, smaller: what should `coverage_tier` carry when there is no percentage? Nullable, or a new variant that names the absence. Either is a schema change on a field agents read.

While fixing this, the human summary line in `crates/cli/src/report/human/health.rs` describes this path as "estimated from export references", which is not where the number comes from for a test-reachable unmatched function.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `df15924cb3ace9155aa431625f7e151d445617a6`.  There
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
{"case_id": "fallow_rs_fallow__2453__df15924",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
