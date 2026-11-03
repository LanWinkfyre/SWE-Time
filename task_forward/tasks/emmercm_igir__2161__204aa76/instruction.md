# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Using the `--dat-combined` option with the zip command doesn’t generate a single archive containing all the ROMs like the documentation says it does.

### Paste the command

`npx -y igir@latest copy zip test --dat '../dats/no-intro/Atari - Atari 2600 (Parent-Clone) (20260322-033038).dat' --input '../roms/Atari - Atari 2600 (Parent-Clone)' --output ./ --dat-combine -vvv`

### Describe the bug

Instead of generating a single ZIP archive with all the source ROMs as the documentation says the `--dat-combined` option should do, a separate ZIP archive is generated for each individual ROM.

### Expected behavior

A single ZIP archive containing all the ROMs in the input directory is generated.

### Debug log

[debug.log](https://github.com/user-attachments/files/26491067/debug.log)

### DAT(s) used

No-Intro Atari 2600 Parent/Clone dat downloaded from Dat-O-Matic, version 20260322-033038

### igir version

v4.3.2

### Node.js version

v24.14.0

### Operating system

Linux, x86-64

### Additional context

The input directory used for the command was previously generated using igir.

In this particular case I’d like to group my collection of Atari 2600 ROMs into one single archive to limit wasted storage space on an exFAT formatted microSD card I’m using for storage, as the 256 kiB cluster size translates to somewhere around 100 MiB of wasted space with the size of this collection, but is desirable for efficiency reasons when dealing with storing newer ROMs.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `204aa76c39d528ca7f5d82d76f1a707394b27813`.  There
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
{"case_id": "emmercm_igir__2161__204aa76",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
