# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
GitHub Action combined mode fails on dupes stats when clone_groups is empty

### What happened?

`fallow-rs/fallow@v2` fails our CI in default combined mode with:

```text
Fallow found 2 issues
Process completed with exit code 1
```

But there are no actionable duplicate findings or source annotations.

The relevant local CLI output is:

```json
{
  "kind": "dupes",
  "schema_version": 7,
  "version": "2.92.1",
  "clone_groups": [],
  "clone_families": [],
  "stats": {
    "total_files": 545,
    "files_with_clones": 4,
    "total_lines": 35615,
    "duplicated_lines": 59,
    "total_tokens": 135437,
    "duplicated_tokens": 189,
    "clone_groups": 2,
    "clone_instances": 5,
    "duplication_percentage": 0.16566053629088867
  }
}
```

The action appears to gate on `.dupes.stats.clone_groups`, so it fails with 2 issues, while the actual `.dupes.clone_groups` array is empty. As a result, GitHub only shows generic `.github` annotations like “Fallow found 2 issues”, with no duplicate group details to fix.

This still happens after upgrading the action input to Fallow `2.96.0`.

### CI details

Workflow snippet:

```yaml
- name: Fallow analysis
  uses: fallow-rs/fallow@v2
  with:
    version: '2.96.0'
    format: sarif
```

Observed action log:

```text
Using fallow version from action input: 2.96.0
Installed fallow 2.96.0
Fallow found 2 issues
ISSUES: 2
Error: Fallow found 2 issues
```

The action revision resolved by GitHub was:

```text
fallow-rs/fallow@v2
SHA: 24a30b1d266f477c30f6878fc9e4c34c00d04d75
```

### Expected behavior

One of these should happen:

1. `stats.clone_groups` should match the reported `clone_groups.length` after filtering, so this case reports `0`.
2. Or the GitHub Action gate should fail based on the actionable clone groups array, not the pre/post-filter summary stat.
3. Or the action should surface the hidden duplicate groups it is counting so the CI failure is actionable.

### Actual behavior

The action fails because `stats.clone_groups = 2`, but the JSON findings array is empty:

```json
{
  "clone_groups": [],
  "stats": {
    "clone_groups": 2
  }
}
```

No source-level annotations are emitted.

### Related issue

This is similar in symptom to #85 because CI says duplication exists while the report/comment does not show duplicate groups, but it appears to be a different root cause.

#85 was about clone groups being filtered out by changed-file scoping due to absolute vs relative paths.

This case happens before any useful annotation/reporting: the dupes JSON itself has an empty `clone_groups` array but non-zero `stats.clone_groups`.

### Workaround

For now we are avoiding default combined mode and using:

```yaml
- name: Fallow analysis
  uses: fallow-rs/fallow@v2
  with:
    version: '2.96.0'
    command: audit
    format: sarif
```

That avoids the combined-mode `.dupes.stats.clone_groups` gate until this is fixed upstream.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1de4f0125e8d5d99dc13639ac579b546a060369d`.  There
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
{"case_id": "fallow_rs_fallow__1250__1de4f01",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
