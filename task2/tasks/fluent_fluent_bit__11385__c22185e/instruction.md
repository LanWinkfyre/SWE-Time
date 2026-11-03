# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_prometheus_scrape plugin missing buffer_max_size config description

## Bug Report

**Describe the bug**
Missing configuration parameter description for buffer_max_size.

**To Reproduce**
```
./fluent-bit -i prometheus_scrape -h

...
buffer_max_size      [EMPTY HERE]              
                                   > default: 10M, type: size
...
```

**Expected behavior**
Above command should show description matching docs for this plugin.

Note, already documented!

**Screenshots**
N/A

**Your Environment**
* Version used: ALL
* Configuration: ALL
* Environment name and version (e.g. Kubernetes? What version?): ALL
* Server type and version: ALL
* Operating System and version: ALL
* Filters and plugins: Prometheus Scrape input plugin

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c22185ef0f6f2270330ea2f5a22289438e7dfb51`.  There
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
{"case_id": "fluent_fluent_bit__11385__c22185e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
