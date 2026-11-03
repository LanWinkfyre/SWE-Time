# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Accessor records named `get x` or `set x` never match their extracted function

Producers disagree about how to name an accessor in a coverage map, and fallow matches only one of the spellings.

For `get area()` on a class, `istanbul-lib-instrument` records the function as `(anonymous_0)`, which fallow resolves positionally. Raw V8 coverage records it as `get area`, and `oxc-coverage-instrument` deliberately mirrors that. Fallow extracts the unit as `area`, so the name never matches and the accessor falls back to a static estimate even though the map measured it.

## Reproduction

Same source, same positions, one field changed:

```
fnMap[0].name = "(anonymous_0)"   ->  area  coverage_source istanbul   coverage_pct 0.0
fnMap[0].name = "get area"        ->  area  coverage_source estimated  coverage_pct null
```

The same divergence applies to setters, and the classes of function affected extend to object-literal properties holding a named function expression and function-valued default parameters.

## Why it matters beyond the accessor

An accessor covered at 100 percent is reported as unmeasured, and in a file no test reaches it draws a CRAP finding it has not earned. It also breaks an invariant the producer side already states: two producers observing the same function are supposed to agree on its identity, and a name prefix makes them disagree.

## What needs deciding

Normalizing on the matcher side (strip a leading `get ` or `set ` before comparing) fixes raw V8 and the oxc instrumenter in one place with one test, and does not disturb anything that already matches. Changing the producer instead would move existing identities. There is also a richer option: prefer the producer's own function-map overlay when a map carries one, which is more work and more correct long term.

Normalization looks like the small correct first move.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4e21f86a386ceae6a2a9dce0ebdd0607e7c2e33d`.  There
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
{"case_id": "fallow_rs_fallow__2456__4e21f86",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
