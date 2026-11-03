# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
DAT file clash handling (for example: for no-intro headered and unheadered NES dats)

### Paste the command

igir copy zip test --dat ~/Downloads/No-Intro*.zip --input ~/Tools/Testing/Input/ --output ~/Tools/Testing/Output/{es}


### Describe the bug

First of all, I know this isn't the place for this, but I've only recently started using igir, and I'm positively impressed by the amount of functionality, the ease of use and the presentation. Thanks for giving us this software!

The actual "bug" (not sure if it qualifies as one):
When I use the No-Intro love pack .ZIP file as dat source, there are, for several systems (Atari 7800 and Nintendo NES comes to mind) dat files included for both headered and unheadered versions.

As igir always matches checksums without the header, and as the output (with / without header) depends on the datfile used, there are, for one romset, two possible dat files and the outcome is somewhat uncertain and possibly destructive, because headers can be removed without the user being aware. igir will still scan and correctly report both dat files.

The workaround is to not use an all-in-one file such as the No-Intro love pack and instead just use the dat files one actually wants.

### Expected behavior

That's difficult to tell. Either an error message (when clashing dat files are found) or some way to clearly define the output behavior would be good. 

### Debug logs

[igir.txt](https://github.com/user-attachments/files/19942204/igir.txt)

### DAT(s) used

No-Intro Love Pack (Standard) (2025-04-27).zip

### igir version

3.4.2

### Node.js version

18.19.1

### Operating system

Linux Mint 22.1 Cinnamon

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ece604bd3de7cbcb4001648440207b57cf98293f`.  There
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
{"case_id": "emmercm_igir__1565__ece604b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
