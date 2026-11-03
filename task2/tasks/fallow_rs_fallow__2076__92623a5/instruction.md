# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Scope inline-review reconciliation for parallel package jobs

## Summary

Fallow's GitHub/GitLab inline-review reconciliation is global to the pull/merge request. Parallel jobs that analyze separate packages therefore treat one another's fingerprints as stale and can resolve one another's discussions.

`FALLOW_COMMENT_ID` scopes sticky summary comments, but it does not scope inline review discussions.

## Reproduction

Run two GitLab CI jobs against the same merge request:

- job A renders/posts `review-gitlab` for package A;
- job B renders/posts `review-gitlab` for package B;
- each package has a distinct finding and a distinct `FALLOW_COMMENT_ID`.

After both jobs have run, rerun either job. `ci post-review` loads every Fallow fingerprint on the MR. The rerun considers the other package's fingerprint stale and resolves that discussion. Parallel runs can race and repeatedly resolve one another's comments.

The same ownership ambiguity applies to GitHub review reconciliation.

## Expected

Independent analysis jobs can declare a stable review scope. Posting, deduplication, and stale-discussion reconciliation only inspect Fallow discussions belonging to that exact scope.

Suggested contract:

- optional `FALLOW_REVIEW_ID` in the CI integrations;
- `meta.review_id` in typed review envelopes;
- a machine-readable review-id marker in posted review bodies;
- scoped runs see only their exact ID;
- unscoped runs see only legacy unscoped discussions, so an old global job cannot resolve newly scoped discussions.

## Compatibility

Single-job projects that leave the ID unset should retain their current behavior for unscoped discussions. The envelope field can be optional without changing the v2 schema discriminator.

## Acceptance criteria

- Two package jobs with different IDs never deduplicate or resolve one another's findings.
- A rerun resolves stale findings only within its own ID.
- Identical finding fingerprints in two scopes remain independent.
- Scoped and legacy unscoped discussions remain isolated.
- GitHub and GitLab posting/reconciliation fixtures cover the behavior.
- Generated schemas, CI templates, and documentation expose the new variable.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `92623a5f54a52e1834318256218ba989efadeefc`.  There
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
{"case_id": "fallow_rs_fallow__2076__92623a5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
