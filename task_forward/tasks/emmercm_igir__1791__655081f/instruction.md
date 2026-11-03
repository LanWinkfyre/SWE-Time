# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
OOM with official MAME DAT

### Paste the command

igir report --dat mame0278.xml --input /media/dirceu/66760EC6760E96C9/Games/Roms/mame --merge-roms nonmerged

### Describe the bug

When I use Igir with other DATS like No-intro or Redump, it works normally.

But when I use it with a MAME DAT (which is larger than the others), I get an error while reading the DAT and the process terminates. I notice a significant RAM consumption. I have 4GB and it consumes up to 3.2GB.



### Expected behavior

I expected the process to go to the end and the rom verification to begin.

### Debug logs

[igir.log](https://github.com/user-attachments/files/21496747/igir.log)

### DAT(s) used

https://github.com/mamedev/mame/releases/download/mame0278/mame0278lx.zip

### igir version

4.1.2

### Node.js version

N/A

### Operating system

Linux Debian 12

### Additional context

<img width="1366" height="714" alt="Image" src="https://github.com/user-attachments/assets/660119f8-1af3-4c8e-8cdf-f7dfe9e559f9" />
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `655081f5c70c78b058c15f920171d9d007270161`.  There
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
{"case_id": "emmercm_igir__1791__655081f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
