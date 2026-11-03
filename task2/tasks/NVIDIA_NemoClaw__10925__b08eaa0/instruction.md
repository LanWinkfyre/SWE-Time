# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
perf(cli): reuse Hermes container observation within health iteration

## Outcome
Reuse one receipt-bound exact-container observation as the precondition for authenticated health within the same polling iteration.

## Parent
Subissue of #10822.

## Security contract
Before credential-bearing health, validate exact container/sandbox/image/labels/name identity, running and unpaused state, status running, and restart policy unless-stopped. Always inspect again after health. Never reuse across OpenShell commands, mutation, sleep, or a later poll.

## Acceptance
- Mismatched/stale/fabricated observations fail before health.
- Each poll gets a fresh pre-observation.
- Each health command gets a fresh post-inspection.
- Drift during health is rejected.
- Runtime evidence shows reduced capture count.
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
{"case_id": "NVIDIA_NemoClaw__10925__b08eaa0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
