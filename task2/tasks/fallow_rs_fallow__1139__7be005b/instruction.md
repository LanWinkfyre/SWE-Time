# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: make JSON summary, metadata, and unsupported flags consistent

## Problem

Running `fallow security` on a real project surfaced a few CLI output consistency issues that make agent review harder:

- `fallow security --help` lists `--explain`, but `fallow security --explain` exits with an invalid-flag JSON error.
- `fallow security --help` lists `--performance`, but `fallow security --performance` exits with an invalid-flag JSON error.
- `fallow security --format json --summary` emits the full finding list instead of a compact JSON summary.
- JSON output does not include enough run metadata for comparison, such as CLI version, elapsed time, config path, enabled categories, or runtime coverage state.
- `unresolved_callee_sites` is only a count, which hides where call resolution is losing precision.

## Suggested improvement

Tighten the `security` command contract:

- Either support `--explain` and `--performance`, or remove them from the command help.
- Make JSON `--summary` emit category counts, severity counts, confidence/reachability buckets, and unresolved counts without full findings.
- Add stable run metadata under a `_meta` or similar object.
- Add sampled unresolved-call diagnostics, for example top unresolved callees/files and reason codes, with caps to avoid huge output.

## Expected result

Agents and CI can compare scans without parsing the whole finding list, and users do not hit help text that advertises unsupported flags.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7be005b9b27684c19b06a22691716ee8e2b08005`.  There
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
{"case_id": "fallow_rs_fallow__1139__7be005b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
