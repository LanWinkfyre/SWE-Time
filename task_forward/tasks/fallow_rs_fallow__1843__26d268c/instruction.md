# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dead-code consumes over 29 GiB and emits no output

## Summary

`fallow dead-code` grows until it exhausts a 32 GiB workstation and never emits output on a private TypeScript project. Updating from 3.1.0 to 3.4.2 did not resolve it. The duplication pass completes normally on the same project.

## Environment

- Fallow: signed `3.4.2` Linux x64 GNU binary installed through npm
- Also reproduced on Fallow `3.1.0`
- OS: Ubuntu Linux x86_64, kernel `7.0.0-27-generic`
- Node: `24.18.0`
- Workstation: 32 GiB RAM, 8 GiB swap

## Reproduction

Unbounded run:

```sh
fallow dead-code --format json --quiet --explain --summary 2>/dev/null
```

Bounded single-rule run after upgrading to 3.4.2:

```sh
timeout --signal=TERM --kill-after=10s 180s \
  prlimit --as=6442450944 -- \
  fallow dead-code --unused-files --format json --quiet --explain --summary \
  2>/dev/null
```

## Observed behavior

### Unbounded 3.1.0 run

- Continued for more than five minutes without output.
- Grew until system RAM reached approximately 29 GiB used.
- Swap grew to approximately 4 GiB used and the SSD saturated with swap I/O.
- Output remained 0 bytes.
- Memory returned immediately after terminating Fallow.

### Bounded 3.4.2 `--unused-files` run

- Aborted with status 134 after 65.75 seconds.
- Maximum RSS: 3,945,248 KiB.
- 1,571,137 minor page faults.
- 100% CPU.
- Output remained 0 bytes.
- The 6 GiB address-space limit prevented system-wide swapping.

The duplication pass completes successfully on the same project, suggesting this is specific to the dead-code graph path rather than analyzer startup generally.

## Expected behavior

The dead-code pass should complete with bounded memory or fail with a diagnostic rather than consuming all available system memory without emitting output.

The repository is private. I can run focused diagnostics requested by maintainers, but cannot publish its source or configuration.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `26d268c16940da3423a558fed32f57b1f02ab08e`.  There
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
{"case_id": "fallow_rs_fallow__1843__26d268c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
