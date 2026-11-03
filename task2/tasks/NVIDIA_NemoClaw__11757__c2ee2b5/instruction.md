# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
fix(portable): recover stopped managed Ollama during interactive launch

## Problem

Portable Hermes interactive `launch` fails with “inference authority … unreachable” when both the sandbox and its exact managed Ollama runtime are stopped. Running the supported sandbox `start` first successfully recovers the same runtime, after which launch works.

Reproduced on the same GFN seat and exact sandbox/container identities with both `a9db662a35eacdc22993271d34a097446a4c30d7` and `6c3837017d6c2811b457ddeffa813aeb832f1e83`. This predates the latest performance changes. Current main `7892d143d282ab0ffb25b0cd1c7ddd228c0a8313` retains the same interactive route-verification path; exact-main regression evidence will accompany the PR.

## Cause and detection gap

Interactive session preparation verifies the existing inference route without using the receipt-owned Ollama recovery used by probe/start. Existing probe recovery coverage does not establish recovery through interactive launch.

## Expected behavior and acceptance

- Interactive launch/connect recover only the exact published, receipt-owned Ollama runtime under the existing lifecycle fence.
- Preserve registry, runtime, route, forward ownership, authenticated health and rollback checks. Reject authority drift and unrelated runtime/listener ownership.
- Healthy inference continues to work. Other providers retain their verification behavior.
- Add regression evidence that fails before the change and passes afterward, including failure paths. Confirm a real prompt and model response after recovery on the seat when feasible.

## Scope

Part of #11573. Independent of forward-verification timing PR #11735 and performance issue #11574. No launcher-script changes, new provider support or arbitrary inference repair.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c2ee2b5eb7f60bf6deec5624ea35a268b9ac1464`.  There
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
{"case_id": "NVIDIA_NemoClaw__11757__c2ee2b5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
