# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
ignoreFindings follow-ups: empty pattern, uncovered result families, unused-pattern hygiene

All four follow-ups on the `ignoreFindings` key from #1991 have landed.

- **Empty pattern is a hard load failure.** Fixed: the empty-body check applies only after an explicit `!`, a bare empty string is delegated to `compile_user_glob` exactly like `ignorePatterns`, with regression tests in both directions.
- **Migration fidelity.** Fixed in #2056: `fallow migrate` states unconditionally that knip's `ignore` is broader than `ignoreFindings`.
- **Unused-pattern hygiene.** Fixed in #2060: human output now lists patterns that matched no finding, following the existing note for policy file globs, plugin manifests, and `unusedComponentProps.ignorePattern`. Exit codes and machine-readable formats unchanged.
- **Result families outside the filter.** Fixed in #2061: `prop_drilling_chains`, `thin_wrappers` and `duplicate_prop_shapes` are source-owned and now honour `ignoreFindings`; `security_findings` and `security_unresolved_callee_diagnostics` stay visible regardless of the pattern, and `docs/backwards-compatibility.md` says so.

  A panel review changed one detail from the recommendation above: `prop_drilling_chains` is suppressed only when every hop file matches, following the documented multi-owner rule used by `circular_dependencies`, rather than anchoring on the first hop the way changed-file filtering does. Anchor filtering would have broken the published `ignoreFindings` semantics.

  The durable part is the exhaustive destructuring helper next to `remove_ignored_dead_code_findings`: a new result field is now a compile error instead of a silent escape.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4e099c8c3caf5584f2e9a7d211d3055ad7b1c40d`.  There
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
{"case_id": "fallow_rs_fallow__2017__4e099c8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
