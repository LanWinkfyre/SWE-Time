# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
OpenTelemetry input return 400 on invalid endpoint instead of 404

## Bug Report

OpenTelemetry input returns 400 on invalid endpoint instead of expected 404

```
HTTP/2 400 
date: Thu, 02 Jul 2026 08:51:59 GMT

error: invalid endpoint
```

**To Reproduce**
 Config:
```
service:
  flush: 1
  log_level: info

pipeline:
  inputs:
    - name: opentelemetry
      match: "*"
      host: localhost
      port: 4318

  outputs:
    - name: stdout
      match: "*"
```
Send request to invalid endpoint

**Expected behavior**
Returned HTTP code is 404


**Your Environment**
tested with version v5.0.8 and master branch
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `46e15a1d3831f82cab4f717b556fe9045844e53f`.  There
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
{"case_id": "fluent_fluent_bit__12032__46e15a1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
