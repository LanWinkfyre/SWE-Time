# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add an identity-preserving health baseline mode for strict regression gates

Shipped in #2064.

`--baseline-mode identity` matches health findings per function identity instead of per file and category, so a new hotspot that replaced an old one in the same file is reported rather than absorbed by the existing allowance. Line shifts and severity improvements stay suppressed, and resolved findings still disappear without a refresh.

The default stays `count`. Identity baselines keep their count buckets so both modes read them, and comparing in identity mode against a count-only baseline is an input error rather than a silent fallback.

### The identity key, and why it is not content-based

A finding's identity is its file path plus its function name. A content hash was considered as a second discriminator to survive renames, and rejected on evidence:

- `source_hash` digests the function's full span, signature line included (`crates/extract/src/complexity.rs:99`), so renaming a `function` declaration changes the hash anyway. It would only have helped for `const name = (...) => {}`, where the binding sits outside the hashed span.
- Measured on a real repository, function renames that left the signature byte-identical were rare and none carried a finding. File moves were the dominant source of churn, and no key addressed those.
- Carrying the hash into `ComplexityViolation` would have added a permanent public output field with no consumer outside this one opt-in mode.

The known limits are documented on the flag itself: renaming or moving a function that is still in the baseline reports it as new, so re-save after that kind of refactor, and functions sharing a name in one file (or unnamed functions) share an identity and can mask each other.

### Follow-ups

- #2062: `baseline_mode` on the MCP health and audit tools, plus a guard so a count save cannot silently drop the identities from an identity baseline
- #2065: warn on partial baseline staleness instead of only on zero overlap
- #2066: neither mode survives file moves, with the measurement that motivated it
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `64b5ac68735d19e0f221cdb45163143b0b79d36f`.  There
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
{"case_id": "fallow_rs_fallow__2010__64b5ac6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
