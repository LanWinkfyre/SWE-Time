# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Health baselines do not survive file moves in either mode

Follow-up to #2010. Both health baseline modes key on the file path, so moving or renaming a file retires every finding it carried and reports the same findings as new at the new path.

`health_bucket_key` uses the relative path in count mode, and path plus function name in identity mode. Neither survives a file move.

### Why this is the part worth measuring

While choosing the identity key for #2010, a measurement on a real repository (vitest, `packages/**/*.ts`, commits since 2025-01-01) found:

- 9 function renames that left the signature line byte-identical, none of which carried a finding at the time
- 20 file renames, of which 4 carried findings, 16 findings in total

So the failure mode the identity key was designed around is rare in that window, while file moves are the dominant source of baseline churn and no mode addresses them. Anyone doing a directory reorganisation has to re-save and loses the record of what was already accepted.

### Open questions

- Whether rename detection at load time is affordable. Git can report renames for a range, but a baseline has no revision attached to it, so the comparison would need a heuristic rather than a git query, or the baseline would need to record the revision it was saved at.
- Whether a content-based key for the file (rather than the path) is a better fit, and how that interacts with the identity key that already lives inside the bucket.
- Whether this should apply to both modes or only to identity mode.

Not urgent. Filed so the measurement above is not lost, since it is the only evidence gathered so far about where baseline churn actually comes from.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `15c77c23dc7c80040bf55f9de35c2d93731cc4b5`.  There
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
{"case_id": "fallow_rs_fallow__2066__15c77c2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
