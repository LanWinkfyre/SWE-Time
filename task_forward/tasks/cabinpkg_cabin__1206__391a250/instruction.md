# Recover the symbolic verification state this change produces

A regression report was filed against `cabinpkg/cabin`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Ship new releases with .deb and .rpm packages


### Discussed in https://github.com/orgs/cabinpkg/discussions/1160

<div type='discussions-op-text'>

<sup>Originally posted by **zkkv** August 31, 2024</sup>
It would be handy to have DEB and RPM binary packages shipped alongside the source code of poac with each release because building from source is rarely fun for users. This could be done via a set of scripts that create the mentioned packages. The scripts can be kept in the source control.</div>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `391a250e11855554027278a5e9cc12b7c76a1ebd`.  There
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
{"case_id": "cabinpkg_cabin__1206__391a250",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
