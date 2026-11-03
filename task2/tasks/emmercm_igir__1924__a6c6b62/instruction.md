# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
"copy + clean" removes files based on input dir

### Paste the command


igir copy zip --dat DATs --output ROMs --dir-dat-name clean --clean-backup ./recycle  --input ~/Downloads

### Describe the bug

I'm seeing strange behavior with "clean".

Depending on the input dir I use, "clean" removes files from the output dir. Why would this happen as I expect if the file exist in the DAT, it should never be removed during a copy operation.


### Expected behavior

"clean" should never remove a file when DAT file does not change.

### Debug logs

[igir_1.log](https://github.com/user-attachments/files/23997826/igir_1.log)
[igir_2.log](https://github.com/user-attachments/files/23997825/igir_2.log)

### DAT(s) used

https://datomatic.no-intro.org/index.php?page=download&op=dat&s=53

### igir version

4.2.0

### Node.js version

v25.2.1

### Operating system

MacOS 15.6.1 (24G90)

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a6c6b62dcff675bd1b9947311d641fe85236fb20`.  There
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
{"case_id": "emmercm_igir__1924__a6c6b62",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
