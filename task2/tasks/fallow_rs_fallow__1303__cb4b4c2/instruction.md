# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
VS Codium extension always reports falsely high numbers on startup

### What happened?

<img width="342" height="42" alt="Image" src="https://github.com/user-attachments/assets/f48df58f-ff0b-4b66-9653-dfbbdc455226" /> → click → 

<img width="314" height="28" alt="Image" src="https://github.com/user-attachments/assets/3adfeedc-bdb5-4333-88fb-43a0a3132599" />

### Reproduction

1. Open a workspace in VS Codium.
2. See the high numbers in the Fallow part of the status bar.
3. Click it.
4. See it run the analysis and change the numbers.
5. Ctrl+Shift+P and "Developer: Reload Window" if you want to repeat steps 2-5 ad infinitum.  (Though it's also true on a cold boot of Codium.)

### Expected behavior

I'd expect the numbers to match.

### Fallow version

2.92.1

### Operating system

Linux

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cb4b4c2fb465ceb89894dc668478e201f090eabd`.  There
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
{"case_id": "fallow_rs_fallow__1303__cb4b4c2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
