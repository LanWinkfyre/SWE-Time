# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Hold the Portable HOME fence during sandbox start (PR #11336)

Parent epic: #11573

## Delivered outcome

Hermes Portable start and the observed recovery paths now use the correct host authority on default and non-default gateway ports.

## Pull request

- Merged PR: #11336
- Merge commit: [`194324d6d`](https://github.com/NVIDIA/NemoClaw/commit/194324d6d07e38fadf9a64d875b09e3c7eb02f8d)

## Changes delivered by this PR

- Hold the current Portable HOME fence during direct `sandbox start` when a matching Hermes receipt exists.
- Bind Hermes onboarding and runtime-provider lifecycle work to the host-scoped Portable state directory, preventing the `18080` gateway lock-path mismatch seen in the seat test.
- Keep transaction-bound `ollama-local` authority out of generic provider publication so its saved version remains stable across restart.
- Route the repaired Hermes lifecycle mutations through OpenShell and reconcile container/OpenShell settlement.
- Finalize a resumed published inference route.
- Accept Podman's native network-inspection schema when validating the existing sandbox network.

## Boundary

#11336 fixed the immediate failures observed in the seat cycle. It did not complete lock-policy consolidation for every lifecycle caller; those follow-ups were delivered by #11482 and #11490.

Status: delivered to `main`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9e07bcfa2bd944c84582ed787a7c1d15a5d6e4b7`.  There
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
{"case_id": "NVIDIA_NemoClaw__11555__9e07bcf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
