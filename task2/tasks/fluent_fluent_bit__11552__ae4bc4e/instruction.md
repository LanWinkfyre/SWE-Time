# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
flb_snappy: harden out_data/out_len NULL checks in flb_snappy_uncompress_framed_data

## Summary

In `src/flb_snappy.c`, the function `flb_snappy_uncompress_framed_data` validates `out_data` and `out_len` for `NULL` **after** the raw/block snappy fallback path. This means a caller passing `NULL` output pointers will be forwarded to `flb_snappy_uncompress` (which will likely crash or behave incorrectly) rather than receiving a clean `-1` return.

The validation of `out_data` and `out_len` should be moved **before** the framed-format detection conditional so that both the raw fallback path and the framed path benefit from the guard.

## Suggested fix

Move the `out_data`/`out_len` NULL checks and the output pointer initialization (`*out_data = NULL`, `*out_len = 0`) to the very top of the function, before the 10-byte stream identifier check.

## Context

- This pre-existing issue was identified during review of PR #11550 (which fixes intermittent decompression failures for raw snappy data).
- It was agreed to track this as a separate issue to avoid expanding the scope of #11550.

## References

- PR: https://github.com/fluent/fluent-bit/pull/11550
- Review comment: https://github.com/fluent/fluent-bit/pull/11550#discussion_r2931985562
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ae4bc4e00acbfae06585930a015c35e66ed18428`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__11552__ae4bc4e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
