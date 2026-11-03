# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(slack): proof workspace omits hoisted fast-uri

## Investigation Summary

- [Messaging providers](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568882853) fails its installed Slack runtime proof with a missing fast-uri module.
- The same failure repeats on [later main](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678904598) and exact candidate 0ddc3ea52 in [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523).
- The installed OpenClaw lock already contains fast-uri. The E2E proof resolves the global OpenClaw symlink without following it, then builds its temporary workspace from the symlink parent instead of the real install root.
- Hoisted production dependencies therefore exist in the installed tree but are absent from the proof workspace.

## Description

The external Slack proof workspace does not mirror the installed OpenClaw dependency layout. Slack startup inside that proof fails before provider behavior can be validated.

Expected: the proof workspace resolves the real installed OpenClaw root and exposes its hoisted production dependencies.

Actual: the proof links only the subtree below the global symlink and cannot resolve fast-uri.

## Reproduction Steps

1. Run the Slack case in the Messaging providers Docker E2E.
2. Start the external installed-runtime proof workspace.
3. Observe Node fail while loading the AJV URI runtime.

## Environment

- GitHub Actions Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943), and [33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523)

## Debug Output

Cannot find module fast-uri from the external Slack proof workspace.

## Acceptance Criteria

- Resolve the real installed OpenClaw package root before constructing the proof workspace.
- Add an installed-tree test that includes a hoisted dependency outside the OpenClaw package subtree.
- Do not add another package or remediation mechanism when the installed lock already contains the dependency.
- Messaging providers passes without workspace-hoisting assumptions.

## Candidate Fix

- [PR #11000 — test(e2e): resolve Slack proof workspace through the real OpenClaw root](https://github.com/NVIDIA/NemoClaw/pull/11000), authored by @AzeelSajjad.
- Status at linkage: open draft.
- #11000 follows the real install root and adds the installed-tree regression test.
- PR #10996 should drop its extra fast-uri packaging and remediation path.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `685eab2f5ac0fbd18c07c44a39143abceac4ca03`.  There
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
{"case_id": "NVIDIA_NemoClaw__10968__685eab2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
