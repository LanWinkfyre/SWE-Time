# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Eliminate remaining Istanbul static fallbacks after v3.20.0

## Description

The v3.20.0 fix from #2442 materially improved downstream coverage matching, but a fresh validation in a private TypeScript monorepo still finds maintained runtime functions that fall back to static estimates.

Against the official v3.20.0 release, the downstream audit reports:

- 3,077 production functions analyzed
- 2,975 matched to Istanbul
- 102 still using static estimates

These aggregate counts motivate the investigation; the private downstream is not an acceptance dependency. This is a follow-up to #2442, not a reopening of that terminal issue.

## Public Reproduction

Create minimal, repository-owned fixtures for each distinct matcher or extraction defect found during diagnosis. Each fixture must fail against the v3.20.0 behavior and pass after the fix without requiring access to a private repository or private artifact.

## Expected Behavior

Every maintained runtime function with a unique, semantically valid Istanbul counterpart uses real Istanbul coverage. Ambiguous or non-runtime units must not receive false coverage attribution.

## Acceptance Criteria

- Add a minimal public regression fixture for every distinct root-cause class addressed by the change.
- Demonstrate that each regression fails before the fix and passes afterward.
- Match every uniquely attributable runtime function in those fixtures without introducing false or ambiguous attribution.
- Preserve rejection of genuinely ambiguous candidates and preserve existing matcher behavior.
- Keep all acceptance evidence reproducible from this public repository alone.
- Pass the focused upstream tests and the full upstream validation suite.
- Ship the fix in an official signed Fallow release.

## Non-blocking Downstream Validation

Sanitized aggregate checks against private downstream inputs may be used as an additional confidence signal, but they are not required for review, merge, or release and must not expose private identifiers or artifacts.

## Environment

- Fallow: official v3.20.0 release, tag target 85d490ce31ada36388dd59f7860716b261b48694
- Coverage format: Istanbul `coverage-final.json`
- Language: TypeScript
- OS: macOS
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ef4231886a47d810896a6d0d1ed5a0f0c0eaa2b5`.  There
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
{"case_id": "fallow_rs_fallow__2448__ef42318",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
