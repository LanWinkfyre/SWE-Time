# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Custom rom path tokens

### Is your feature request related to a problem?

I personally like to have some sort of custom sorting, f.e. I don't want to mix aftermarket rom dumps with "regular" ones. I could use the dat file names as folder names, but I'd actually prefer my old, custom ones.

### Describe the solution you'd like

I'd prefer a way of creating my own {token}, or some rules which would handle which rom dumps go where. For example:
[...]
Atari - Atari 2600 (Aftermarket) -> a2600am
Bandai - WonderSwan -> ws
Bandai - WonderSwan -> wsc
[...]

### Additional context

igir already provides tokens such as {es} or {batocera} to match the folder structure used by popular tools. There is also the --dir-mirror option, but that is not flexible enough to handle properly adding new files to the collections.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `781b5da4fa4c44ed40f9de3ff2ea2e4a937828db`.  There
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
{"case_id": "emmercm_igir__1566__781b5da",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
