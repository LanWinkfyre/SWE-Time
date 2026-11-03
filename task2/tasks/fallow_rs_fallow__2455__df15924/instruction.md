# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
A coverage map that does not join is indistinguishable from code that has no coverage

Three materially different situations produce byte-identical output today:

1. the coverage map does not join at all (wrong root, container path prefix, stale artifact),
2. the map joins but nothing in it can be attributed to the functions fallow extracted,
3. the map joins and honestly records that nothing ran.

All three render as `coverage_source: "estimated"` with a null percentage, and the human report prints one line:

```
CRAP scores use Istanbul coverage where matched (0/5 functions); unmatched functions are estimated from export references.
```

A user whose paths did not line up gets the same report as a user whose code genuinely has no tests, and the first situation is the one with the highest recovery cost. In CI, a build-tooling change that breaks the path join makes the coverage feature go quiet without any signal, and the health trend keeps moving as though the denominator had not changed.

## What is missing

- **No per-file join signal.** Nothing reports how many files in the map matched an analyzed file. That number is the whole diagnosis for the path-mismatch case.
- **The function ratio counts test files.** The `N/M` above includes functions in test files, so it cannot be read as a coverage-join health metric even by hand.
- **`coverage_source_consistency` is ambiguous.** It reports `uniform` when everything matched and also when nothing did, which makes the one machine-readable provenance signal useless exactly when a consumer needs it.

## Prior art in the repository

The runtime coverage path already solves the human half of this: `render_capture_quality_warning` in `crates/cli/src/report/human/health_runtime.rs` warns when captured data looks degraded. The Istanbul path has no equivalent.

## What needs deciding

- Does a zero join rate stay a note, become a warning, or become a failure? A gate flag would let CI treat "coverage was supposed to be here" as an error rather than silently scoring everything as unmeasured.
- Does the JSON gain a join block (files in map, files joined, functions attributed), and does the existing function ratio get its denominator corrected to production functions? That is a change to a field consumers already read.
- Progressive disclosure keeps the healthy case unchanged: a field always, a human line only when the join is degraded, detail behind `--explain`.

Related: the scoring half of this is in #2453, and the two should not be merged. Fixing the score does not make a failed join visible.
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
{"case_id": "fallow_rs_fallow__2455__df15924",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
