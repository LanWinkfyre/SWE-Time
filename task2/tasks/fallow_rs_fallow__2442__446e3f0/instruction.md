# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Match Istanbul body locations and skip bodyless overloads

## Description

Fallow can classify maintained TypeScript functions as statically estimated even when the Istanbul coverage map contains the corresponding runtime function. A fresh downstream audit against current source and a current merged coverage map found 2,985 maintained functions, with 2,868 Istanbul matches and 117 static estimates.

The 117 residuals classify as:

- 110 functions whose structurally matching anonymous Istanbul entry is available through the function body location (loc.start), while Fallow indexes the producer effective line and declaration start.
- 2 nested anonymous functions where multiple candidates tie under the current distance heuristic; the safe result is the strictly innermost containing span while sibling ties must remain rejected.
- 5 bodyless TypeScript overload declarations that are emitted as complexity units even though they have no runtime body and therefore cannot have an Istanbul fnMap entry.

This extends the location-matching class previously addressed in #370.

## Steps to Reproduce

1. Analyze maintained TypeScript containing multiline/nested anonymous functions and bodyless overload declarations.
2. Generate Istanbul coverage for all runtime functions.
3. Run Fallow health with complexity, file scores, and the Istanbul coverage map.
4. Inspect coverage_source and the summary counts.

A downstream reproduction using Fallow 3.17.0 consistently reports 2,868 Istanbul matches and 117 maintained estimates. The same relevant matcher and extractor source is unchanged in 3.18.0 and current main.

## Expected Behavior

- Runtime functions with an unambiguous Istanbul body-location match use real Istanbul coverage.
- Nested anonymous functions select a unique strictly innermost containing span, without crediting sibling ties.
- Bodyless TypeScript overload declarations are not emitted as runtime complexity units.
- The downstream maintained set reports no static coverage fallback.

## Actual Behavior

Fallow misses body-location aliases, rejects two resolvable nested cases as ambiguous, and emits five bodyless overload declarations. All 117 then silently use static coverage estimates.

## Environment

- Fallow: 3.17.0 downstream; relevant files verified byte-identical in 3.18.0 and current main
- Coverage: Istanbul coverage-final.json
- Language: TypeScript
- OS: macOS

## Acceptance Criteria

- Add focused regression fixtures for body-location aliases, nested anonymous spans, sibling-tie rejection, and bodyless overload declarations.
- Index safe Istanbul body-location aliases.
- Resolve only unique strictly innermost containing anonymous candidates.
- Continue rejecting ambiguous sibling candidates.
- Skip bodyless Function nodes when producing runtime complexity units.
- Preserve existing matching behavior and pass the full upstream test suite.
- Validate the downstream reproduction changes from 117 maintained estimates to zero without false attribution.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `446e3f0a55c68c95ef765cfe5c872e1e8a16e509`.  There
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
{"case_id": "fallow_rs_fallow__2442__446e3f0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
