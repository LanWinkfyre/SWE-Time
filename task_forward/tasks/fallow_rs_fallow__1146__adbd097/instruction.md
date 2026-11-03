# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: extend source-backing from one hop to bounded multi-hop local taint

## Motivation

The `tainted_sink` detector already back-traces a sink argument to an untrusted source through one same-module hop (template-literal / string-concat / object-literal initializers, #1095), and ranks candidates with an `arg-level` vs `module-level` `taint_confidence` tier (#1092, #1093). The remaining accuracy gap for active candidates is multi-hop local flow: a source that reaches a sink through two or three intermediate local bindings is currently only `module-level` (weak) or missed.

## Proposed

- Extend the existing one-hop source-backing to a bounded N-hop (cap 2 to 3) intra-module chain over local bindings.
- Keep it name-based and syntactic (ADR-001), conservative, and keep the doctrine: rank, never gate; candidate, not verdict; prefer false negatives (#885).
- Keep the `arg-level` tier as the strong tier; multi-hop source-backed flows are `arg-level`.
- Consume the function-local relation layer (#1142) as the substrate rather than bespoke binding walks, once that layer exists.

## Relationship to existing work

- Complementary to #1138 (literal and constant propagation before sink matching): that resolves constant values into sinks; this propagates untrusted-source taint across local bindings. Different direction; they should compose, not overlap.

## Acceptance

- A source reaching a sink through up to N local-binding hops is `source_backed` with `arg-level` confidence.
- The hop cap is explicit and documented; over-cap chains degrade to `module-level`, never a false `arg-level`.
- No new false positives on the existing security fixtures; the false-negative-over-false-positive posture is preserved.

Relates to: #1142 (substrate), #1095 (one-hop foundation), #1092, #1093 (confidence tiers), #1138 (complementary constant propagation).

Size: M.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `adbd09776e877b539ff5777a44e131aea9d21e9e`.  There
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
{"case_id": "fallow_rs_fallow__1146__adbd097",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
