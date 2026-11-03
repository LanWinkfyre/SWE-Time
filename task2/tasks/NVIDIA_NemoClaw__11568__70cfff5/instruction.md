# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Cap managed Hermes auxiliary request tokens (PR #11578)

Parent epic: #11573

## Outcome

Preserve explicit output-token limits for Hermes auxiliary requests on NemoClaw managed inference.

## Pull request

- PR: #11578
- Verified commit: [`9c888152d`](https://github.com/NVIDIA/NemoClaw/commit/9c888152d8d2d7021df51f7489feee3e59c31566)

## Defect

Hermes v0.20.6 drops `max_tokens` from auxiliary OpenAI-compatible requests to custom endpoints. On NemoClaw's managed `inference.local` endpoint, that also removes the small title-generation limit and can make an auxiliary request consume a much larger token budget and appear to hang.

## Safety boundary

Apply the image-build patch only to `inference.local`; preserve Hermes behavior for other custom endpoints and verify the patcher and updated probe through integrity hashes.

## Completion

- [x] Open and link a focused PR to `main`.
- [x] Pass 64 focused auxiliary/image-probe tests, CLI and plugin builds, and CLI type-check.
- [ ] Pass full CI and review.
- [ ] Record the merged `main` commit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `70cfff5f946a9bb31d1147f78ffbda914a2efaa2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11568__70cfff5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
