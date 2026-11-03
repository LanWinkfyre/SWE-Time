# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
CodSpeed report generation fails since the walltime benchmark joined the simulation run

`CodSpeed Performance Analysis` has failed on every commit since 2026-07-27, with the bot posting:

> Unable to generate the performance report. There was an internal error while processing the run's data.

It reads like a CodSpeed outage, but the evidence points at our workflow.

## When it broke

| Commit | Date | `walltime` in `bench.yml` | CodSpeed check |
|---|---|---|---|
| `45f1642a21b` | 24 Jul | 0 | **success** |
| `20972d541b1` | 27 Jul 12:30 | 2 | **failure** |
| every commit since | | 2 | failure |

`git log -S walltime -- .github/workflows/bench.yml` returns exactly one commit: `20972d541b1` ("feat: add stable type-aware TypeScript analysis"), which is also the first failing commit. The last green check is the commit immediately before it.

## What the workflow now does

`.github/workflows/bench.yml` uploads **two different CodSpeed instruments under one workflow run per commit**:

- `benchmark-fast` / `benchmark-full` shards: `mode: simulation` (bench.yml:119, :196)
- `benchmark-type-aware`: `mode: walltime` (bench.yml:147)

Every job succeeds and every job uploads. The walltime job reports `Collected walltime data for 2 benches` and `Performance data uploaded`; the simulation shards report `Measurement mode: Simulation` and `Performance data uploaded`. So the failure is not collection or upload, it is report assembly: CodSpeed gets simulation and walltime measurements for the same commit and cannot reconcile them into one comparison.

## Why the PR reports looked inconsistent

PR #2003 got a working comparison while main was already failing, which is what made this look intermittent. The main-branch check has been failing continuously since 12:30 on 27 Jul regardless.

## Suggested fix

Split the walltime benchmark into its own workflow so each CodSpeed run carries a single instrument. Worth confirming against CodSpeed's docs on multiple runs per commit before implementing, since the exact reconciliation rule is theirs, not ours.

Two smaller things noticed while tracing this:

- `benchmark-type-aware` does not declare `id-token: write`, unlike the simulation jobs. The upload currently succeeds, so this is not the cause, but the asymmetry looks unintended.
- Several main commits have no benchmark run at all (`882f31056de`) or a cancelled one (`d73cee930b1`, `d3b7350e7fc`), because a following push cancels the in-flight run via the concurrency group. That leaves gaps in the baseline chain independent of this bug.

## Note

This check has been failing all day and was waved through as a CodSpeed-side outage on #2014, #2020 and #2023, each admin-merged past it. The benchmark jobs really do all pass, which is what made that reading plausible, but the check itself has been red since the walltime job landed and should not have been treated as noise.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2ffd3a327285b23e4163bd8b867d8b784a5d7f4e`.  There
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
{"case_id": "fallow_rs_fallow__2024__2ffd3a3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
