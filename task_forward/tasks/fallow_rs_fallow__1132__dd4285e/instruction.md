# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: make --summary affect JSON output

## Summary

`fallow security --summary --format json` currently emits the same JSON as a full security run. That makes `--summary` ineffective for agents and CI jobs that need compact machine-readable output.

Observed with `fallow@latest` 2.91.0 on June 9, 2026.

## Repro

```bash
npx --yes fallow@latest security --format json --quiet > /tmp/security-full.json
npx --yes fallow@latest security --summary --format json --quiet > /tmp/security-summary.json
cmp /tmp/security-full.json /tmp/security-summary.json
```

Actual: `cmp` reports identical files.

Current JSON keys are still the full envelope:

```text
kind,schema_version,security_findings,unresolved_edge_files,unresolved_callee_sites
```

## Expected

`--summary --format json` should emit a compact summary envelope instead of full `security_findings`.

Suggested shape:

```json
{
  "kind": "security",
  "schema_version": "2",
  "summary": {
    "security_findings": 0,
    "by_severity": {},
    "by_category": {},
    "unresolved_edge_files": 0,
    "unresolved_callee_sites": 0
  }
}
```

The exact shape can vary, but it should be documented and schema-backed.

## Acceptance criteria

- JSON summary output is smaller than full JSON and omits individual findings.
- Human `--summary` behavior stays intact.
- Schema, generated TS contracts, and tests cover the summary JSON shape.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `dd4285e9bdc35772909fdad8095a00e4378b9c6b`.  There
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
{"case_id": "fallow_rs_fallow__1132__dd4285e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
