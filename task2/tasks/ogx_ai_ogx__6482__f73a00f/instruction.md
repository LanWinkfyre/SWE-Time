# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Batch API processing does not apply user policy restrictions

### System Info

Review type: Static source and test coverage review
OGX: 1.0.2
OGX commit: 9424b4d9e5eca99bfc79a6e0004e28adf5f58704
Affected component: Inline batches reference provider

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The source contains:

```text
TODO SECURITY: this currently works with configured api keys, not with x-ogx-provider-data or with user policy restrictions
```

### Error logs

Second security note is present in the path:
https://github.com/ogx-ai/ogx/blob/v1.0.2/src/ogx/providers/inline/batches/reference/batches.py#L653

```text
TODO SECURITY: review body for security issues
```

### Expected behavior

### Expected result

User identity, provider data and policy restrictions should be preserved and enforced for queued batch requests. Clarify the current security model, add authorization tests for batch processing and prevent batch requests from bypassing the policy layer.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f73a00f47083741128030653fcbf64ea71949dfe`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "ogx_ai_ogx__6482__f73a00f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
