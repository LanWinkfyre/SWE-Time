# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Dev container broken, because trixie has removed moby-cli

I'm looking to work a little on the fluent-bit project. I saw that your project provides a devcontainer.json, so I decided to give that a try.

The following steps were run:

1. git clone a fresh copy of the master branch of the fluent-bit repo.
2. Open the repo in vscode.
3. Press Ctrl+Shift+P and run the "Dev Containers: Reopen in Container" action.

If you try to do this, you end up with an error like this in the container build log:

```
0.201 (!) The 'moby' option is not supported on Debian 'trixie' because 'moby-cli' and related system packages have been removed from that distribution.
0.201 (!) To continue, either set the feature option '"moby": false' or use a different base image (for example: 'debian:bookworm' or 'ubuntu-24.04').
0.201 ERROR: Feature "Docker (Docker-in-Docker)" (ghcr.io/devcontainers/features/docker-in-docker) failed to install! Look at the documentation at https://github.com/devcontainers/features/tree/main/src/docker-in-docker for help troubleshooting this error.
```

The least intrusive option of these two is to simply set "moby" to false, so I suggest to simply change that.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `acad02a531bbfc882f5dddc44b05915318769efb`.  There
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
{"case_id": "fluent_fluent_bit__11556__acad02a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
