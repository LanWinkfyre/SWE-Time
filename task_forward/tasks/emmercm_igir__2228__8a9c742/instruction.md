# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
CHDs report as FOUND but files do not exist.

### Paste the command

npx igir report `
     --dat "Z:\Dats\MAME\MAME 0.287 CHDs (merged).zip" `
     --input "Z:\Roms\MAME\CHD"

### Describe the bug

CSV report shows every CHD file as FOUND - only 1 file in the folder (not worried about unused in this paste)

...
MAME CHDs (merged),zone3d,FOUND,,false,false,true,false,false,false,false,false,false,false,false,false,false
MAME CHDs (merged),zoofari,FOUND,,false,false,true,false,false,false,false,false,false,false,false,false,false
MAME CHDs (merged),zooo,FOUND,,false,false,true,false,false,false,false,false,false,false,false,false,false
,,UNUSED,Z:\Roms\MAME\CHD\agro.chd,false,false,false,false,false,false,false,false,false,false,false,false,false

### Expected behavior

Missing files to be marked MISSING in the CSV report

### Debug log

[debug.log](https://github.com/user-attachments/files/27733868/debug.log)

### DAT(s) used

https://github.com/pleasuredome/pleasuredome/raw/gh-pages/mame/MAME%200.287%20CHDs%20(merged).zip

### igir version

v5.0.1

### Node.js version

v22.14.0

### Operating system

Microsoft Windows [Version 10.0.19045.7291]

### Additional context

Redump, nointro, and mame roms seem to work fine, just mame CHDs (and software list CHDs) are showing FOUND but have no filename, files do not exist.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8a9c7426c7c4c3dcdc02637c0adc136ba7539b0a`.  There
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
{"case_id": "emmercm_igir__2228__8a9c742",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
