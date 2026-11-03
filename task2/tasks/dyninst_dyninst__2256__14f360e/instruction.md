# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
Incorrect container iteration in IntervalMap

**Describe the bug**

In both 
https://github.com/dyninst/dyninst/blob/14f360e7814e0a9606a3499b26317f68403da539/dataflowAPI/rose/util/IntervalMap.h#L224

and

https://github.com/dyninst/dyninst/blob/14f360e7814e0a9606a3499b26317f68403da539/dataflowAPI/rose/util/IntervalMap.h#L236

The iteration through be through otherIter intead of other
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `14f360e7814e0a9606a3499b26317f68403da539`.  There
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
{"case_id": "dyninst_dyninst__2256__14f360e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
