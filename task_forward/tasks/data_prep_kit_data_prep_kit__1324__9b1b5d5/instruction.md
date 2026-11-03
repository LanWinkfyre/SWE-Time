# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Bug] Spark transforms fail with PySpark 4.0.0

### Search before asking

- [x] I searched the [issues](https://github.com/data-prep-kit/data-prep-kit/issues) and found no similar issues.


### Component

transforms/doc_id

### What happened + What you expected to happen

A new release of pyspark==4.0.0 was released on May 22nd  and create incompatibility with current version of JDK 11 currently in use. The error shows as:
Error: A JNI error has occurred, please check your installation and try again
Exception in thread "main" java.lang.UnsupportedClassVersionError: org/apache/spark/launcher/Main has been compiled by a more recent version of the Java Runtime (class file version 61.0), this version of the Java Runtime only recognizes class file versions up to 52.0

### Reproduction script

step 1: clone repo
step 2: modify data-processing-lib/spark/requirements.txt to have pyspark==4.0.0
step 3: navigate to transforms/universal/doc_id and run make test-src

### Anything else

For now, we set PySpark dependency to be pyspark<=3.5.5

### OS

Ubuntu

### Python

3.11

### Are you willing to submit a PR?

- [x] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9b1b5d54617c4d8d552548c70f375ace79803334`.  There
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
{"case_id": "data_prep_kit_data_prep_kit__1324__9b1b5d5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
