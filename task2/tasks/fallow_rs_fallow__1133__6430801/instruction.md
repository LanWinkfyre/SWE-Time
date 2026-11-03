# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: preserve arg-level and source-backed ranking after severity sorting

## Summary

Security ranking has improved with `reachability.taint_confidence` (`arg-level` versus `module-level`), but the CLI applies an additional severity and location sort after core ranking. That can discard finer-grained ordering inside the same severity tier.

Observed in current source and with `fallow@latest` 2.91.0 on June 9, 2026.

## Current behavior

The core ranking sorts by entry reachability, source-backed evidence, module-level source reachability, blast radius, boundary crossings, and dead-code context.

After that, the CLI runs a separate sort by severity and location. This keeps high/medium/low ordering, but within a tier it can move a weaker module-level candidate ahead of a stronger arg-level/source-backed one if the path sorts earlier.

## Expected

Within each severity tier, preserve or reapply the security-specific ranking signals:

1. Runtime hot candidates.
2. Arg-level/source-backed candidates.
3. Module-level source-reachable candidates.
4. Higher blast radius and boundary crossings.
5. Active code before dead-code-linked candidates.
6. Path, line, col, category only as deterministic tiebreakers.

## Acceptance criteria

- CLI output keeps severity grouping without losing arg-level/source-backed ordering inside a severity tier.
- Tests cover two same-severity findings where the later path has stronger arg-level/source-backed evidence and must sort first.
- The schema/docs continue to frame this as ranking, not exploitability proof.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `643080188c563ea9294448624d951f1d6b49603f`.  There
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
{"case_id": "fallow_rs_fallow__1133__6430801",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
