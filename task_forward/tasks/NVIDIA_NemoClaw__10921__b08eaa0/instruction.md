# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
perf(cli): complete Hermes recovery timing coverage

## Outcome
Ensure detailed currentness and exact-container inspection timing is emitted through every normal Hermes Portable stopped-recovery path.

## Parent
Subissue of #10822.

## Scope
Record credential-free numeric durations and counts for receipt, socket, OpenShell executable, Podman executable, transaction comparison, container capture, guards, parsing, and identity comparison. Preserve recovery behavior.

## Acceptance
- Normal connect/recovery and requalification paths propagate timing callbacks.
- Timing callback failures cannot change recovery.
- Output excludes arguments, output, endpoints, credentials, tokens, and environment values.
- Regression tests cover every callback path.

## Status
PR #10839 merged the primary instrumentation. Remaining work is to verify/complete normal-path callback propagation against current main.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b08eaa0844dc2e972fbfa2806590668802d449b4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10921__b08eaa0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
