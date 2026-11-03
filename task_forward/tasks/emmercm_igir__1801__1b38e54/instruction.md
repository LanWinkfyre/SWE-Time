# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Enable comprehensive error reports with a command line option

### Is your feature request related to a problem?

Yes, reporting bugs for igir does take quite a long time with all the info we need to additionally provide.

### Describe the solution you'd like

igir should be able to provide all the required info in one file, so that we could just enable creating this file with a command line option. We could then attach this file to any bug, add a short description, and be done with it.

### Additional context

This would also mean less work for you in the long run, as you would have to deal with a lot less incomplete bug reports.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1b38e547881f10fd77698456ca524fd4e8e6094f`.  There
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
{"case_id": "emmercm_igir__1801__1b38e54",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
