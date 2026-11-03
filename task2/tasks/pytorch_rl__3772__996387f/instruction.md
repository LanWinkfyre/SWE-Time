# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] CrossGroupCritic TensorDict Module for groups with different obs/action specs

##Solution + Motivation 
CrossGroupCritic — a single new TensorDictModule that acts as a drop-in critic. It does three things:

Per-group encoder (nn.Linear per group) — projects each group's observations to a shared embedding dim d. This is what handles heterogeneous obs shapes.
Shared MLP trunk — concatenates all groups' embeddings along the agent dim [B, n_a+n_b, d] and processes the joint representation.
Per-group output heads — splits the trunk output back by group size and writes a value key for each group.

##Why? 

MAPPOLoss doesn't change at all. You just pass CrossGroupCritic as the critic_network argument and call set_keys with the right group value key. Two MAPPOLoss instances (one per group) share the same critic object — gradients from both flow into it before each optimiser step.

Ad-hoc teamwork: add a detach_groups=["fixed_policy_group"] flag — the fixed group's encoder output is detached before the trunk, so the critic still sees their observations for a better baseline, but no gradient flows back into anything the fixed policy touches.

Scope: 1 new file (cross_group_critic.py), 2 export additions, 1 test file. Zero changes to existing MAPPO/IPPO code.

Fixes #3748
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `996387f029820bf7bd81b333154988388344ced8`.  There
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
{"case_id": "pytorch_rl__3772__996387f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
