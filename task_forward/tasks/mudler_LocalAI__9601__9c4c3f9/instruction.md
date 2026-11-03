# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
parameter to change /tmp default download temp to /..../tmp

**Is your feature request related to a problem? Please describe.**
somewhat, /tmp is on the root partition which has limit size

**Describe the solution you'd like**
a paramater to set /tmp as a custom path or set it relative to the localai directory

**Describe alternatives you've considered**
tried out a few parameters to no avail

**Additional context**
default /tmp is on the root partition which has limit size
the size limit is because of automation and manageability
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9c4c3f9d8f9109f151e60550dd02657d15650292`.  There
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
{"case_id": "mudler_LocalAI__9601__9c4c3f9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
