# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Discrete offline CQL

## Motivation

Both offline and online in continuous/discrete action space CQL are implemented in sota-implementations, except for **discrete offline CQL**.

## Solution

Add support for discrete offline CQL. This would complete the CQL sota-implementations in the repository and benefit users working with discrete action space offline RL benchmarks and datasets.

## Alternatives

Use existing open-source discrete offline CQL implementations from other repositories.
However, this alternative may not maintain the same code quality, integration, or consistency as a native sota-implementation within torchrl.

## Additional context

Adding discrete offline CQL will bring the repository in line with other SOTA RL codebases and help the community benchmark and reproduce results for discrete action spaces in offline RL.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `009f4ce1692bf8a9ac49f7a0c7886179e9fec655`.  There
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
{"case_id": "pytorch_rl__3097__009f4ce",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
