# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
graph: cap or fall back when test-reachability profile count explodes

Follow-up to #2068. `TestReachabilityIndex`/`ProfileWorklist` (crates/graph/src/graph/reachability.rs) scale with the number of distinct mask combinations across test-root replacements: storage is O(files * profile_count / 64) and propagation cost grows with profile count. There is no upper bound and no fallback to the cheaper legacy bitset path when profile_count grows large; tests cover up to 65 profiles.

A large monorepo where many test files each mock a unique module set could plausibly reach thousands of profiles. Precedent exists in the same area: `re_export_transition_safety_cap` uses an explicit safety cap for an analogous blowup risk.

Proposal: add a profile-count cap; above it, fall back to legacy coarse reachability (fail-open, matching pre-#2068 behavior) and record a diagnostic. Add a stress test at a realistic large-profile scale.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `83c54f36bf3c9400be14f433eb2a5e5965e0e39c`.  There
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
{"case_id": "fallow_rs_fallow__2084__83c54f3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
