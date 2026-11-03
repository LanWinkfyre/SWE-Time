# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Error in version 5.0

### Paste the command


igir --help

### Describe the bug

Hello, I'm a Linux user (Debian 13). I downloaded the binary for the new version of Igir (5.0) to my machine (Linux AMD64) and checked that all execution permissions were correct, but when I run Igir in the terminal I get the following error:

[1] 67056 illegal hardware instruction

All other versions of Igir have always worked on my machine. My configuration is as follows:

I7 3517u

Intel HD 4000 Graphics

4GB RAM DDR3


### Expected behavior

I was hoping everything would work as before.



### Debug log

[Example.txt](https://github.com/user-attachments/files/26932997/Example.txt)

### DAT(s) used

_No response_

### igir version

5.0

### Node.js version

_No response_

### Operating system

Linnux Debian 13

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7c7d547c2ad7ca895475332e8ad83c09c3584774`.  There
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
{"case_id": "emmercm_igir__2206__7c7d547",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
