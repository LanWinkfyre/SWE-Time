# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: add sampled diagnostics for unresolved callees

## Summary

`fallow security` reports `unresolved_callee_sites` as a count, but does not show where the unresolved callee sites are concentrated or why resolution failed. This makes it hard to improve detector coverage or explain blind spots to agents.

Observed with `fallow@latest` 2.91.0 on June 9, 2026.

Example top-level output:

```json
{
  "unresolved_callee_sites": 6035
}
```

## Expected

Add a bounded diagnostic sample for unresolved callee sites, suitable for JSON consumers and human debugging.

Suggested additive shape:

```json
{
  "unresolved_callee_sites": 6035,
  "unresolved_callee_diagnostics": {
    "sampled": [
      {
        "path": "src/example.ts",
        "line": 42,
        "col": 10,
        "reason": "computed-member",
        "expression_kind": "member-expression",
        "callee_preview": "client[method]"
      }
    ],
    "top_files": [
      { "path": "src/example.ts", "count": 12 }
    ],
    "by_reason": {
      "computed-member": 20,
      "dynamic-dispatch": 7
    }
  }
}
```

Exact names can change. Keep the data compact and deterministic.

## Acceptance criteria

- JSON exposes bounded unresolved callee diagnostics without source-code windows.
- Human summary can mention top reason or top file when diagnostics are present.
- Diagnostics are stable, capped, and safe for large repos.
- Existing `unresolved_callee_sites` remains for backwards compatibility.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2e00978bd13ace7f98ac1f9d0eb9782ad50c76aa`.  There
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
{"case_id": "fallow_rs_fallow__1134__2e00978",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
