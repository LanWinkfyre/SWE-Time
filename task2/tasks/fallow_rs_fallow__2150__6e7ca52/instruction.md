# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Complexity breakdown in Vue template

### What happened?

The fallow extension reports a complexity issue in a Vue template with v-if/else, but it does not show the breakdown.

<img width="485" height="396" alt="Image" src="https://github.com/user-attachments/assets/4029c6cd-c650-425b-aadd-d312fc073aa2" />

### Reproduction

Repro : https://github.com/Ericlm/fallow-vue-complexity

### Expected behavior

It should display the conditions that increase the complexity, just like in script setup:

<img width="447" height="410" alt="Image" src="https://github.com/user-attachments/assets/e1d2b31d-0fff-4a8e-a025-5cbcaf57ebe3" />

### Fallow version

extension: 3.14.0

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6e7ca52dfe6002365142ca3541f6cd96472cfb1b`.  There
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
{"case_id": "fallow_rs_fallow__2150__6e7ca52",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
