# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Bug: Cursor file links are double-encoded for Next.js dynamic route folders

### What happened?

Fallow VS Code extension generates invalid file URIs for paths containing [ and ] (e.g. Next.js App Router dynamic route folders).

The path segments are encoded twice:
[activityId] -> %255BactivityId%255D

instead of:
[activityId] -> %5BactivityId%5D

As a result, Cursor cannot resolve the file.

Cursor error:
cannot open file:///.../src/app/activities/%255BactivityId%255D/layout.tsx. Detail: Unable to read file '...\src\app\activities\%5BactivityId%5D\layout.tsx' (Error: Unable to resolve nonexistent file '...\src\app\activities\%5BactivityId%5D\layout.tsx')

### Reproduction

1. file structure: src/app/activities/[activityId]/questions/[questionId]/components/matching-cards-section.tsx
2. click open file from fallow extension tab

### Expected behavior

_No response_

### Fallow version

2.91.0

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `351085e83521d2a0fe7e4060920d6e2b4e48dbe7`.  There
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
{"case_id": "fallow_rs_fallow__1160__351085e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
