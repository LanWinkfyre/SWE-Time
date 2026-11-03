# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_tail: missing three config parameter descriptions

## Bug Report

**Describe the bug**
Three configuration parameter descriptions are missing:

1. `watcher_interval` 
2.  `progress_check_interval`
3.  `progress_check_interval_nsec` 

**To Reproduce**
```
./fluentbit -i tail -h   

...
watcher_interval
                                       > default: 2s, type: time

progress_check_interval
                                       > default: 2s, type: time

progress_check_interval_nsec
                                       > default: 0, type: integer
...
```

**Expected behavior**
Expect to have descriptions for all available plugin configuration parameters.

**Screenshots**
None.

**Your Environment**
* Version used: All
* Configuration: All
* Environment name and version (e.g. Kubernetes? What version?): All
* Server type and version: All
* Operating System and version: All
* Filters and plugins: in_tail

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9b32a6af645bcef12db4e164d7a3d2616be0dcdb`.  There
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
{"case_id": "fluent_fluent_bit__11403__9b32a6a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
