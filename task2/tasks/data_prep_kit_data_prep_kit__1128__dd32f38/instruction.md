# Recover the symbolic verification state this change produces

A regression report was filed against `data-prep-kit/data-prep-kit`.  The report is quoted verbatim below.

## Report

```
[Feature] Allow users to define and use specialized data access classes

### Search before asking

- [x] I searched the [issues](https://github.com/IBM/data-prep-lab/issues) and found no similar issues.


### Component

Other

### Feature

Currently, the open source DPK only support local storage and S3. When adding a new data access class, users need to create their own Factory class in addition to implementing their own data access class and go through the CI/CD process for both the data access class and for the Factory. Further, credentials and secrets are currently passed as a command parameter that creates a security concern.

In order to reduce the amount of code required from the developer and enhance security of user defined storage, It would be desirable to:

1. Allow developers to add their own data access class while leveraging (without any changes to ) the existing Factory class. 

2. Allow the developers to deploy their own data access classes and modules to the run-time environment without having to go through our own Ci/CD process.

3. allow the users to implement more secure procedures for sharing credentials and secrets (via environment variables or other mechanisms as they see fit).

### Are you willing to submit a PR?

- [x] Yes I am willing to submit a PR!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `dd32f384bcbb6d26ab7bb7065a6c495a0a5c0891`.  There
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
{"case_id": "data_prep_kit_data_prep_kit__1128__dd32f38",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
