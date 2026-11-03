# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
README benchmarks may be outdated after jscpd Rust rewrite

Hi,

First of all, thanks for building Fallow.

I noticed the benchmark section in the README compares Fallow against jscpd and reports 20–30x speed improvements.

Those numbers appear to be based on the previous Node.js implementation of jscpd. Since jscpd v5, the project has been completely rewritten in Rust and performance characteristics have changed significantly.

The current benchmark results are available here:

https://github.com/kucherenko/jscpd/blob/master/benchmark/BENCHMARK.md

According to the published benchmark suite, jscpd v5 is 24–37x faster than the previous implementation and scans large repositories in a few seconds rather than tens of seconds.

Would it be possible to rerun the benchmarks against the latest jscpd release and update the README if the results differ?

I'd be happy to help reproduce the benchmark environment or provide any additional details.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0eb7b4925fe623ee4eabec54eeeb42965fa1534f`.  There
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
{"case_id": "fallow_rs_fallow__1316__0eb7b49",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
