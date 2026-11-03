# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: add version, timing, and safe config metadata to JSON output

## Summary

`fallow security --format json` currently lacks the metadata that other JSON-producing analysis commands expose, such as CLI version and elapsed time. That makes scan regression comparisons harder across releases and configs.

Observed with `fallow@latest` 2.91.0 on June 9, 2026.

Current top-level keys:

```text
kind,schema_version,security_findings,unresolved_edge_files,unresolved_callee_sites
```

Missing compared with other JSON surfaces:

- `version`
- `elapsed_ms`
- `_meta` when `--explain` is supported
- Safe config context, for example enabled categories and relevant rule severity, without dumping raw private config paths or values

## Expected

Add metadata that lets agents compare security scans across time and versions.

Suggested additive shape:

```json
{
  "kind": "security",
  "schema_version": "2",
  "version": "2.91.0",
  "elapsed_ms": 123,
  "config": {
    "security_client_server_leak": "warn",
    "security_sink": "warn",
    "categories_include": [],
    "categories_exclude": []
  }
}
```

Do not include absolute config paths, raw config file contents, license identifiers, repository identifiers, or source snippets.

## Acceptance criteria

- Security JSON includes `version` and `elapsed_ms` like the other analysis JSON envelopes.
- If `--explain` is implemented for security, JSON includes a security-specific `_meta` block.
- Any config metadata is allowlisted and privacy-safe.
- Schema and generated output contracts are updated.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b8495b2425a493247cc471921ae82a3fb534f71a`.  There
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
{"case_id": "fallow_rs_fallow__1135__b8495b2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
