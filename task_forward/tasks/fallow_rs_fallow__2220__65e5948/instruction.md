# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit: observability for new-only duplication demotion

Follow-up to #2164. Clone groups whose instances contain no added line are now demoted from introduced to inherited under `--gate new-only`, but the demotion is invisible: nothing in the output says a group was demoted or why.

Proposed additive improvements:
- a `duplication_demoted` counter in the audit attribution block,
- an `--explain` line naming each demoted group and the rule that demoted it,
- document that an opt-in shared diff index takes precedence over the merge-base worktree diff for the demotion decision, and that a diff derived from a narrower base can over-demote.

Also from the same review, worth a separate look: a removal inside a region that creates a clone group escapes the added-line check (real but rare), and the demotion key is non-monotonic on the health axis.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `65e5948403ebe35025c568de564fc96590fc1e7c`.  There
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
{"case_id": "fallow_rs_fallow__2220__65e5948",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
