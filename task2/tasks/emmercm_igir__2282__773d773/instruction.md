# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Linux and64 binariy failed since v5.1.0

### Paste the command

`igir`

### Describe the bug

Running the [binary release 5.1.0  for Linux 64](https://github.com/emmercm/igir/releases/download/v5.1.0/igir-5.1.0-Linux-amd64.tar.gz) failed with
```
$ igir-5.1.0 
error: Cannot find module 'yargs/package.json' from '/$bunfs/root/index.js'

Bun v1.3.14 (Linux x64 baseline)
 
``` 

### Expected behavior

For the program to run standalone without an error.

### Debug log

[debug.log](https://github.com/user-attachments/files/28787431/debug.log)

### DAT(s) used

N/A

### igir version

v5.1.0

### Node.js version

N/A

### Operating system

Debian GNU/Linux 13 (trixie) AMD64

### Additional context

No debug log available as the error happens before any igir command is executed.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `773d773c00ceb637fa47c9e93f08528f3d693f7e`.  There
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
{"case_id": "emmercm_igir__2282__773d773",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
