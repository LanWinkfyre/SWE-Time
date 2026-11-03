# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_gpu_metrics: updated config parameters descriptions

## Bug Report

**Describe the bug**
Various updates needed to ensure the config parameters of gpu metrics input plugin are clear and concise.

**To Reproduce**
./fluent-bit  -i gpu_metrics -h

**Expected behavior**
Expect clear and concise descriptions but existing descriptions are not informative.

**Screenshots**
N/A

**Your Environment**
* Version used: all
* Configuration: all
* Environment name and version (e.g. Kubernetes? What version?): all
* Server type and version: all
* Operating System and version: all
* Filters and plugins: in_gpu_metrics

**Additional context**
N/A
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7ded9ae04e1693718edb8bc88e8b8d154c77d314`.  There
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
{"case_id": "fluent_fluent_bit__11236__7ded9ae",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
