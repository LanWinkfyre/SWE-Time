# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_elasticsearch: missing http config parameter description.

## Bug Report

**Describe the bug**
`http2` config parameter is missing description for this plugin.

**To Reproduce**
fluent-bit -i elasticsearch -h 

**Expected behavior**
Expect a description for all configuration parameters.

**Screenshots**
N/A

**Your Environment**
* Version used: all
* Configuration: all
* Environment name and version (e.g. Kubernetes? What version?): all
* Server type and version: all
* Operating System and version: all
* Filters and plugins: all

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `10ebd3a354f2a052ac865960145fda844b3b120e`.  There
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
{"case_id": "fluent_fluent_bit__11225__10ebd3a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
