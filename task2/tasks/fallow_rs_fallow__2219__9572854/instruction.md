# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
config: end-to-end test for the explicit private-type-leaks seam

Follow-up to #2170. The fix records explicit configuration of `private-type-leaks` in a serde-skipped `RulesConfig` flag set by `FallowConfig::from_merged` and read by the CLI's type-aware default. Tests cover the halves separately (config-load tests; unit tests on a hand-built resolved config), but nothing asserts the full path: `FallowConfig::load` of a real config file -> `resolve` -> type-aware default application. That seam regresses silently on a config refactor (no compile error; the flag just becomes false and the default force-enables the rule again).

Also worth covering in the same change: the flag is `serde(skip)`, so any serialize/deserialize round-trip of `FallowConfig` silently drops it. No production path round-trips today; add a doc comment on the field warning about it and a regression test so a future round-trip reintroducing the bug fails loudly. And `RulesConfig` is a pub struct in the published `fallow-config` crate without `non_exhaustive`; the new pub field was a source-breaking change for downstream struct literals, worth a note in the crate docs.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95728543e804a0e4a4a0ca9dd239f328c6adde4d`.  There
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
{"case_id": "fallow_rs_fallow__2219__9572854",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
