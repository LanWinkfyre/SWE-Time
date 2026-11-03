# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
All commands immediately terminating with exit code 255

### Paste the command

All commands (e.g., `igir --help`)

Similar issue (described below) with all commands run through `npx` (e.g., `npx igir@latest --help`)

### Describe the bug

When running any command (e.g., `igir --help`) the program terminates with no output, with exit code 255.

Running with npx (e.g., `npx igir@latest --help`) immediately outputs "Illegal instruction" and terminates.

### Expected behavior

Expecting command to run as intended (e.g., for `--help` to output the help message).

### Debug logs

The program has no output (including when run with the `-vvv` option).

### DAT(s) used

N/A

### igir version

4.2.1

### Node.js version

v22.14.0

### Operating system

Debian GNU/Linux 12

### Additional context

Also tried with 4.2.1 and 4.2.0.

I have run the program successfully on my Windows installation so I don't think I am doing anything wrong in execution. I assume it's some kind of dependency issue?
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `962fb80c8e9bf7eb830becdffbded22100333e8c`.  There
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
{"case_id": "emmercm_igir__1788__962fb80",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
