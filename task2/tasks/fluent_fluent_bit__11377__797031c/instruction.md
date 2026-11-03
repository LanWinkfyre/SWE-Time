# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_prometheus_remote_write: missing descriptions for configuration parameters

## Bug Report

**Describe the bug**
Missing help descriptions for the `http2`, `buffer_max_size`, and `buffer_chunk_size` configuration parameters, currently `NULL` or empty strings. 

**To Reproduce**

- Steps to reproduce the problem:
```
./fluent-bit -i prometheus_remote_write -h
```

**Expected behavior**
Expect to have help descriptions for all configuration parameters.

**Screenshots**
N/A

**Your Environment**
* Version used: ALL
* Configuration: ALL
* Environment name and version (e.g. Kubernetes? What version?): ALL
* Server type and version: ALL
* Operating System and version: ALL
* Filters and plugins: in_prometheus_remote_write

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `797031cc30d2845b4dcb36cece6d6f2dd363d430`.  There
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
{"case_id": "fluent_fluent_bit__11377__797031c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
