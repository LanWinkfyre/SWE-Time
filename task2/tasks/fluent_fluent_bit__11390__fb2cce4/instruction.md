# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_splunk: splunk input plugin is missing configuration parameter descriptions

## Bug Report

**Describe the bug**
  Missing descriptions:
```
http2                        NULL
buffer_max_size     "" 
buffer_chunk_size  "" 
tag_key                    ""   
```
 
 There is also a typo in the store_token_in_metadata description - "matadata" should be "metadata".

**To Reproduce**
- Steps to reproduce the problem:
```
./fluent-bit -i splunk -h
```

**Expected behavior**
Each config param should have a description.

**Screenshots**
N/A

**Your Environment**
* Version used: ALL
* Configuration: ALL
* Environment name and version (e.g. Kubernetes? What version?): ALL
* Server type and version: ALL
* Operating System and version: ALL
* Filters and plugins: in_splunk

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fb2cce46c2a7b6e631027fb338837a033184d918`.  There
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
{"case_id": "fluent_fluent_bit__11390__fb2cce4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
