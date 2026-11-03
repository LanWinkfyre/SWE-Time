# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(forward): deployment verification cannot reach new host forwards

## Investigation Summary

- The exact-candidate [PR #11071 E2E run](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) tested commit `0ddc3ea52efe8a5d63099b92f43cbe0a43c88a01`.
- Six targets completed sandbox startup but failed deployment verification because a newly requested dashboard or Hermes API host forward refused connections:
  - [Cloud onboard](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163747249)
  - [Hermes Bedrock](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750026)
  - [OpenClaw provider switch](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750184)
  - [OpenClaw Bedrock](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750391)
  - [OpenClaw skills](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163751120)
  - [Hosted inference](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163751707)
- Hermes Bedrock lost both dashboard port 18789 and API port 8642. The OpenClaw targets lost dashboard port 18789.
- This is distinct from #11074, where a second onboarding rejects an already-bound expected listener.
- #10385 has the same Hermes API symptom on Ubuntu 24.04 GPU, but this run also affects CPU Docker targets and OpenClaw. Confirm whether they share one forward-lifecycle defect before deduplicating.

## Description

A new sandbox reaches the deployment-verification stage, but its host forwards are not accepting connections. Several otherwise unrelated E2E targets therefore fail before testing their feature-specific behavior.

Expected: a requested ForwardTcp service is discoverable and reachable before deployment verification begins.

Actual: verification immediately reports `port forward not working (connection refused)`.

## Acceptance Criteria

- Capture the OpenShell forward list and start result when verification sees a refused connection.
- Distinguish a listener that is still settling from a failed or missing ForwardTcp service.
- Add a bounded readiness rule without adopting an unknown listener.
- Confirm whether the Hermes API failure in #10385 has the same cause.
- All six affected exact-head targets pass their initial deployment verification repeatedly.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1c6031569639a8ac2668552da11bc9e9d1ef9cd2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11084__1c60315",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
