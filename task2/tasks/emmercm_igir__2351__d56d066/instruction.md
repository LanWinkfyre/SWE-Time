# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Add Nuon to the romm directory structure

### Is your feature request related to a problem?

Importing from the Nuon standard DAT file does not result in CHDs being put in the "nuon" directory.

**Redump DAT file**: http://redump.org/discs/system/nuon/

**Example command**: .\igir.exe move zip -d '.\dats\Redump\VM Labs - NUON - Datfile (11) (2025-01-23 03-39-43).zip' -i .\import\Nuon\ -o "roms/{romm}"

**Romm support platforms**: https://docs.romm.app/4.9.0/resources/snippets/supported-platforms/ 
(Nuon is on the list).



### Describe the solution you'd like

The CHD or ISO files from the Nuon DAT file placed in the "nuon" directory when using the {romm} directory key.

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d56d06660b07b313a40edec719aa91f8129751ed`.  There
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
{"case_id": "emmercm_igir__2351__d56d066",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
