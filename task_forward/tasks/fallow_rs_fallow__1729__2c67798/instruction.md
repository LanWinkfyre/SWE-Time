# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add stylelint config migration for styling audit thresholds

## Summary

Add a migration helper that reads an existing Stylelint configuration and suggests equivalent or adjacent Fallow styling-audit settings where Fallow owns the same quality signal.

## Scope

- Detect common selector, nesting, and important-usage thresholds from Stylelint configs.
- Print a proposed Fallow config patch instead of mutating by default.
- Keep the boundary clear: do not migrate formatting, syntax, vendor-prefix, declaration-order, or value-style rules that belong to Stylelint.
- Document unsupported rules as intentionally left to Stylelint.

## Acceptance criteria

- The command handles JSON, JS, and package.json Stylelint config locations when they can be read safely.
- It maps only supported styling-quality thresholds into Fallow config.
- It reports unsupported Stylelint rules without pretending Fallow replaces them.
- It has fixture coverage for at least one Stylelint config and one no-op config.

## Notes

This is a follow-up convenience for teams adopting styling audit. It is not required for the v3 styling claim.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2c67798f2629db09e82117ce345130c1c822bf6d`.  There
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
{"case_id": "fallow_rs_fallow__1729__2c67798",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
