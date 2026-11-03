# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
inference: Model Router E2E selects a retired Nemotron 3 Nano endpoint

## Investigation Summary

- The [Model Router target](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568885222) receives HTTP 410 for `nvidia/nemotron-3-nano-30b-a3b` on `3076188279c0ea657ec77aeeabebf1f82061eaaf`.
- The same target and model fail again on [later main](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678907845).
- The service reports the model reached end of life on 2026-09-01 and no fallback route is configured.
- Draft [PR #10918](https://github.com/NVIDIA/NemoClaw/pull/10918) proposes refreshing the pool to `openai/gpt-oss-20b`; this issue tracks the release gate until the fix is merged and verified.

## Description

The checked-in Model Router pool selects a retired provider model, making every routed request fail deterministically.

Expected: routed E2E uses a supported model and has a maintained fallback/retirement process.

Actual: LiteLLM returns HTTP 410 with no fallback.

## Reproduction Steps

1. Run the provider-routed Model Router E2E.
2. Send the qualification prompt through the default pool.
3. Observe selection of `nvidia/nemotron-3-nano-30b-a3b` and HTTP 410.

## Environment

- GitHub Actions Docker
- NVIDIA hosted inference
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Acceptance Criteria

- Remove the retired model from every active pool/catalog/fixture.
- Verify the replacement with a trusted provider-routed response.
- Add a proactive model-retirement or availability gate.
- Full-suite Model Router target passes after #10918 or its replacement lands.


## Candidate Fix

- [PR #11070 — fix(inference): update Model Router pool](https://github.com/NVIDIA/NemoClaw/pull/11070), authored by @rsliter.
- Status at linkage: open draft.
- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) again returns HTTP 410 for nvidia/nemotron-3-nano-30b-a3b with no fallback.
- #11070 replaces the retired route with openai/gpt-oss-20b and keeps one provider-routed completion proof.
- PR #10918 is closed and superseded. Keep this issue open until #11070 merges and its exact target passes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `94bb868ea0f3e98533b06196def74b7559a1d1d4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10969__94bb868",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
