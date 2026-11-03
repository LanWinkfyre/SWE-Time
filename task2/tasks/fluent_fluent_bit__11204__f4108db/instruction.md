# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Blob input plugin - Missing descriptions for various configuration options.

## Bug Report

**Describe the bug**
Blob input plugin - Missing descriptions for various configuration options.

- Steps to reproduce the problem:
Run the plugin with -h flag and see several empty descriptions listed.

**Expected behavior**
Expect all configuration options to have short descriptions.

**Screenshots**
N/A.

**Your Environment**
* Version used: 4.2
* Configuration: N/A
* Environment name and version (e.g. Kubernetes? What version?): N/A
* Server type and version: N/A
* Operating System and version: N/A
* Filters and plugins: Blob input plugin

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f4108db65e876fadbabac459aa11990c5440550a`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__11204__f4108db",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
