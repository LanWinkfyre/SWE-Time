# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
test(e2e): census and ratchet transitive live assertion surface

Parent: #10920

## Problem

NemoClaw does not have a deterministic inventory or no-growth check for assertions in the live E2E suite. Contributors can add assertions directly, move them into live companion modules, or replace several checks with another assertion form without making the increased failure surface visible.

Epic #10920 records the fixed reference baseline at `fe18b2f004e2304c52db33cf7bb5895828197f9a`: 95 collected E2E tests, 2,184 direct Vitest `expect(...)` calls, and 2,677 `expect(...)` calls across live tests and companion modules. This issue must regenerate the implementation baseline from the current `main` commit and explain any difference from that reference.

## Outcome

Add a repository-owned assertion census that reports the assertion surface of every live E2E test and a ratchet that rejects assertion growth while Epic #10920 reduces the existing baseline.

The census must make assertion relocation visible. Moving a product assertion from a test body into a live companion module must not reduce the target's reported transitive count.

## Scope

This issue includes:

- deterministic discovery of `test/e2e/live/**/*.test.ts`;
- static parsing of TypeScript and JavaScript assertion forms;
- resolution of repository-local live companion imports for each test;
- stable per-file, per-test, and suite totals;
- separate direct and transitive counts;
- a checked-in current-main baseline;
- a no-growth ratchet that accepts reductions and rejects increases;
- human-readable and machine-readable output;
- focused tests for discovery, parsing, import traversal, stable ordering, malformed input, and budget failures;
- contributor guidance for running and updating the check.

## Initial assertion forms

The first census must count these forms without counting comments or inactive text as TypeScript assertions:

- Vitest `expect(...)` matcher chains;
- Node assertion calls;
- calls to assertion helpers whose names begin with `assert` or `expect`;
- product-state `fail(...)` and `throw` conditions in live companion modules;
- independently checked fields in large object comparisons where the static shape is available.

The report must identify generated shell, Python, and JavaScript probe strings that contain detectable assertion conditions. The initial ratchet may report these separately when a reliable one-to-one assertion count is not available. It must not silently classify them as zero.

## No assertion laundering

The implementation must not lower a count when an assertion moves:

- from a test into a reachable live helper;
- from a matcher into `assert*`, `expect*`, `fail`, or a conditional `throw`;
- into a large object comparison with independently checked fields;
- into a generated probe that the census can detect.

Shared companion assertions may contribute to more than one test's transitive count. Suite totals must also report each source assertion once so shared code does not inflate the global baseline.

## Non-goals

This issue does not:

- remove or rewrite existing E2E assertions;
- change E2E behavior, target selection, jobs, matrices, or scheduling;
- enforce Epic #10920's final 50-percent budget yet;
- add live E2E execution;
- infer whether an existing assertion is useful or belongs lower in the test stack;
- change production code.

## Acceptance criteria

- [ ] One command emits a deterministic human-readable census.
- [ ] One command emits deterministic JSON for repository tests and automation.
- [ ] The census reports collected test files, direct assertion counts, transitive companion counts, and suite totals.
- [ ] The census resolves repository-local imports without executing live E2E modules.
- [ ] Comments and ordinary strings do not count as TypeScript assertions.
- [ ] Shared live companions count toward each consuming test's transitive surface and once in suite totals.
- [ ] Detectable generated-probe assertions are visible in a separate report category.
- [ ] The checked-in baseline identifies the current `main` commit used to produce it and explains its relationship to Epic #10920's fixed reference baseline.
- [ ] The ratchet accepts unchanged or reduced counts.
- [ ] The ratchet rejects new test files or changed files that increase the direct, transitive, or suite assertion surface without an explicit reviewed baseline update.
- [ ] The ratchet reports the file or test, previous count, current count, and delta for each failure.
- [ ] The implementation does not use a regex-only parser for TypeScript or JavaScript syntax.
- [ ] Focused tests cover supported assertion forms, transitive imports, cycles, shared helpers, stable ordering, malformed sources, generated-probe detection, passing reductions, and failing increases.
- [ ] `npm run checks:repository` runs the ratchet.
- [ ] `test/README.md` or the owning E2E contributor guidance explains how to run the census and how a remediation PR records reductions.
- [ ] The PR records the current-main census, the fixed Epic #10920 reference, and any baseline difference.

## Quality and security constraints

- The tool must read repository files only. It must not execute E2E modules or generated probes.
- Repository-relative paths must be normalized and constrained to the checkout.
- Symlinks and paths outside the repository must fail closed.
- Malformed source, unresolved live companion imports, and import cycles must produce deterministic results. Cycles must not cause repeated counting or unbounded traversal.
- The baseline must not contain source text, secrets, environment values, or generated test artifacts.

## Validation plan

- Focused repository tests for the census and ratchet.
- `npm run checks:repository`.
- Repository-wide validation required for a new repository check.
- No live E2E run is required because this issue changes deterministic repository tooling and does not change live behavior.

## Related work

- #10920 owns the 50-percent assertion reduction and quality-preservation rules.
- #10517 owns the existing initial high-cost pruning work.
- #9159 owns broader E2E reliability and contributor guidance.
- #7912 owns E2E runtime, runner cost, and scheduling.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b08eaa0844dc2e972fbfa2806590668802d449b4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10934__b08eaa0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
