# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
add option to skip ROM trimming detection

### Is your feature request related to a problem?

Toward the end of a report run, I'm staring at ```Detecting ROM trimming``` which is doing the following in the background:

```
chdman extracthd --output /tmp/igir/20250723-112741/chd/qwhWhX/gdj_jaa_2007071100 --input <chd_path>
```

It seems it's going to do this for every single CHD, which is a bit costly.  I don't see an obvious option in the latest 4.1.1 release that allows skipping of this feature.

### Describe the solution you'd like

Ideally an option would be provided to skip this very costly process.

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `eea6c290b8c860ecc86486b743fefe56df839657`.  There
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
{"case_id": "emmercm_igir__1776__eea6c29",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
