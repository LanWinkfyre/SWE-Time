# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Atari Jaguar CD not correct directory

### Paste the command

.\igir.exe move zip -d '.\dats\Redump\Atari - Jaguar CD Interactive Multimedia System - Datfile (38) (2026-04-03 15-50-49).zip' -i .\import\JagCD\ -o "roms/{romm}" --debug-log "debug.log"

### Describe the bug

When importing using the Redump "Atari - Jaguar CD Interactive Multimedia System - Datfile" the {romm} format puts the files in the "phillips-cd-i" directory, it should be "atari-jaguar-cd".

The regex in the code (consoleTokens.json) seems to look for 
"datNameRegex": "/CD[ -]?i/i",

Matches because "Jaguar CD Interactive"

The Jaguar CD seems to be missing from the list.

### Expected behavior

Jaguar CD images put into "atari-jaguar-cd" directory.

### Debug log

[debug.log](https://github.com/user-attachments/files/29403732/debug.log)

### DAT(s) used

http://redump.org/datfile/ajcd/

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
{"case_id": "emmercm_igir__2344__d56d066",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
