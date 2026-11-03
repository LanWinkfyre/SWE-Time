# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
zip command fails in igir-4.1.2-Linux-amd64.tar.gz

### Paste the command

```
./igir copy zip \
--input "/mnt/NAS02/EMUS/roms/TEST/roms/" \
--dat "/mnt/NAS02/EMUS/roms/TEST/dats/*.dat" \
--output "/mnt/NAS02/EMUS/roms/TEST/zip/"
```

### Describe the bug

Using the zip command with the Linux amd64 binary throws a "TypeError: zlib_1_1_default.Deflater is not a constructor" error while trying to zip a file.


### Expected behavior

Files from the input directory are zipped in the output directory.

### Debug logs

[igir.log](https://github.com/user-attachments/files/21790894/igir.log)

### DAT(s) used

https://datomatic.no-intro.org/index.php?page=download&s=26&op=pc_list

### igir version

4.1.2

### Node.js version

N/A

### Operating system

Manjaro Linux

### Additional context

It looks like igir 4.1.x Linux binaries are missing zlib. The command worked in 3.4.2 and 4.0.0 but fails with the same error from 4.1.0 onward.

`npx igir@latest` version works as expected.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c8d37e5ceabb2d3bc7dbe63f3605cdc4b5ccf64c`.  There
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
{"case_id": "emmercm_igir__1815__c8d37e5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
