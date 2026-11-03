# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Apply Kubernetes filter on fluentbit internal logs input plugin

**Is your feature request related to a problem? Please describe.**
Can't see kubernetes metadata on fluentbit internal logs.

**Describe the solution you'd like**
Enable Kubernetes filter to work on fluent bit internal logs input.  As fluentbit runs as daemonset in Kubernetes, it is useful to see its metadata.

**Describe alternatives you've considered**
none, either than not use the metadata.

**Additional context**
With many fluentbit instances in kubernetes cluster, it helps filtering logs per daemonset.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c2b1cfd5f5b3530d613c167fc999a7df4eb2eabb`.  There
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
{"case_id": "fluent_fluent_bit__11741__c2b1cfd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
