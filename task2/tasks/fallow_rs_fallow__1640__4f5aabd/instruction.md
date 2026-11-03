# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
fix(unused files): package.json missing false positive

### What happened?

I have the following in my `package.json` file

```json
  "commit-and-tag-version": {
    "bumpFiles": [
      {
        "filename": "app/android/app/build.gradle",
        "updater": "app/scripts/gradle-updater.cjs"
      }
    ]
  }
```

Which will use the `gradle-updater.cjs` file when running auto tag version (using the [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) library

### Reproduction

1. Create an "unused" file
2. Reference it in the `package.json` 
3. This will be listed as unused file

### Expected behavior

_No response_

### Fallow version

2.102.0

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4f5aabde8eda855175aee7c0e1dbd695f31e9923`.  There
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
{"case_id": "fallow_rs_fallow__1640__4f5aabd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
