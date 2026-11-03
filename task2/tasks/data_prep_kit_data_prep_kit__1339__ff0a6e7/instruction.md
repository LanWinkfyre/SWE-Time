# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Feature] Pyarrow upgrade needed for data-processing-lib

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

Python Runtime, Other

### Feature

https://github.com/data-prep-kit/data-prep-kit/blob/9dc88012795ab7dc53f61f1899afd946362a14b2/data-processing-lib/python/requirements.txt#L4

I'm currently running into this warning below when installing my dependencies due to this requirements.txt

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
data-prep-toolkit 0.2.5 requires pyarrow==16.1.0, but you have pyarrow 20.0.0 which is incompatible
```

The data-prep toolkit has an older version of pyarrow, which conflicts with an internal package I have which requires `pyarrow<21.0.0,>=17.0.0`. 

An upgrade of the pyarrow package would be appreciated!

### Are you willing to submit a PR?

- [ ] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ff0a6e768d4f548554d7dae67300852b3b885b13`.  There
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
{"case_id": "data_prep_kit_data_prep_kit__1339__ff0a6e7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
