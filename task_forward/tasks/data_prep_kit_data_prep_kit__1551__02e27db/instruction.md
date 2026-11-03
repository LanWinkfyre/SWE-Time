# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Bug] Excessive [INFO] logging with new rich-based logger

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

Other

### What happened + What you expected to happen

After the addition of PR #1519 , there seems to be excessive INFO messages that shows up when running notebook cells. ex:
`/data-prep-kit-pii-imagenotebook/recipes/PII-image/venv/lib/python3.12/site-packag
es/dpk_people/transform.py:256 - parameters are : {'model_path': None, 'mode': 'blur', 'threshold': 0.6, 
'batch_size': 50}
taskName=Task-64
11:20:16 [INFO] 
/data-prep-kit-pii-imagenotebook/recipes/PII-image/venv/lib/python3.12/site-packag
es/data_processing/runtime/execution_configuration.py:91 - pipeline id pipeline_id
taskName=Task-64
11:20:16 [INFO] 
/data-prep-kit-pii-imagenotebook/recipes/PII-image/venv/lib/python3.12/site-packag
es/data_processing/runtime/execution_configuration.py:94 - code location {'github': 'UNDEFINED', 'build-date': 
'UNDEFINED', 'commit_hash': 'UNDEFINED', 'path': 'UNDEFINED'}
taskName=Task-64`

These messages seems to show the line number of code, and seems more helpful if it were [DEBUG] rather than [INFO] as it produces too much output. 
cc: @roytman 

### Reproduction script

N/A 

### Anything else

_No response_

### OS

MacOS

### Python

3.12

### Are you willing to submit a PR?

- [ ] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `02e27db406c72368dc349907ab0ae1b066e71a7f`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `dev`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "data_prep_kit_data_prep_kit__1551__02e27db",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
