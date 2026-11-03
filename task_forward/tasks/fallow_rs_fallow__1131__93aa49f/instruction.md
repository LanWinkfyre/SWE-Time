# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: hide or honor unsupported global flags in help

## Summary

`fallow security --help` lists global flags that `fallow security` then rejects. The command should either support those flags or omit them from the security help surface.

Observed with `fallow@latest` 2.91.0 on June 9, 2026.

## Repro

```bash
npx --yes fallow@latest security --help | rg -- '--explain|--performance'
npx --yes fallow@latest security --explain --format json --quiet
npx --yes fallow@latest security --performance --format json --quiet
```

Actual JSON errors:

```json
{"error":true,"message":"--explain is not valid with `fallow security`.","exit_code":2}
{"error":true,"message":"--performance is not valid with `fallow security`.","exit_code":2}
```

## Expected

Pick one contract and make help, parsing, and output agree:

- Preferred: support `--explain` and `--performance` for `security`, matching the rest of the JSON analysis commands.
- Acceptable fallback: hide these globals from `security --help` and keep rejecting them.

## Acceptance criteria

- `security --help` no longer advertises flags that are rejected by `security`.
- Regression coverage checks the help or parse contract for `--explain` and `--performance`.
- JSON error behavior stays structured if a flag remains unsupported.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `93aa49fc19329a3d901505b7c5e43a5a97d04e98`.  There
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
{"case_id": "fallow_rs_fallow__1131__93aa49f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
