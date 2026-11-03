# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Health baselines rot silently: warn on partial staleness, not just zero overlap

Follow-up to #2010. A saved health baseline degrades as the codebase moves, but the only signal today is all-or-nothing.

`load_health_baseline` warns once, and only when `overlap_entries == 0`. A baseline that still matches half its buckets says nothing at all, so the gate quietly protects less and less over time while still reporting green.

This matters more now that `--baseline-mode identity` exists. Identity buckets are per function rather than per file and category, so there are far more of them and each one is more fragile: a rename, a move, or a file rename retires a bucket. Partial rot is the normal state of an identity baseline, and the current warning cannot express it.

Suggested shape: report how many saved buckets matched nothing on this run, on stderr, in human output only. Something like `N of M baseline entries matched no current finding; re-save to refresh`. Exit codes and machine-readable output unchanged.

Two things to decide:

- whether this is unconditional or gated behind a threshold, since a small amount of drift is normal and a note on every run becomes noise people stop reading
- whether the count is enough, or whether it should name a few example buckets so the reader can tell "we deleted that code" from "we renamed it and the baseline is now lying"

Related: #2062 covers protecting an identity baseline from being silently overwritten by a count save.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `15c77c23dc7c80040bf55f9de35c2d93731cc4b5`.  There
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
{"case_id": "fallow_rs_fallow__2065__15c77c2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
