# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Option to always (single disks too) create .m3u files. Ex. --extract-output-playlist always

### Feature Request.

Allow to create .m3u playlist for all games extracted, not just multidisks games.

### Describe the solution you'd like

Sometimes it is nessary to use only single format for detecting games with emu front. 
Mixing sub folders, bin, cue can create mess in parsed library onscreen.

Please allow to create .m3u like playlist option do, but for any extracted .cue/.bin folder pair.

Example:

```bash
    igir copy extract playlist \
    --extract-output-playlist always \
    --dat "/mnt/emulation_nas/registry/dat/PS/*.dat" \
    --input "/mnt/emulation_nas/registry/roms/PS/" \
    --output "/media/ONION/Roms/PS/" \
    --dir-game-subdir always
```

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a092370031636fb5b9b6050ef8145a4238bb40ce`.  There
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
{"case_id": "emmercm_igir__1742__a092370",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
