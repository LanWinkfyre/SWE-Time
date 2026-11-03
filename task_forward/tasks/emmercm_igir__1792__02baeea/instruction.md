# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Patch candidate not being generated for zipped game

### Paste the command

igir move zip test clean -vvv --dat 'dats/**/*.dat' --input inbox/ --input roms/ --output roms/ --patch patches/ -D

### Describe the bug

I'm trying to use igir's support for patching roms with a GBA rom hack. I'm zipping my roms as recommended by igir's docs, but that seems to be messing up the logic for matching the CRC32 in the patch's filename to the appropriate rom. If I unzip the rom, then igir will match it and patch the file and zip both the original and the patched one. But then it gets cleaned up in the next run because now the original rom is zipped and it doesn't match anymore.

### Expected behavior

The patch should be matched to the correct rom even if the rom is zipped, and subsequent runs of igir with the clean action should not remove the patched rom.

### Debug logs

[igir.log](https://github.com/user-attachments/files/21501494/igir.log)

### DAT(s) used

_No response_

### igir version

4.1.1

### Node.js version

v22.17.0

### Operating system

NixOS unstable

### Additional context

The CRC I'm using in the filename matches the one I see in Ark if I open the zipped rom.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `02baeea35aa5018c87baa17d8e803194ccea60fd`.  There
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
{"case_id": "emmercm_igir__1792__02baeea",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
