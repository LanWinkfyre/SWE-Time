# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(messaging): accepted provider extras breadcrumb is not emitted

## Investigation Summary

- [Messaging providers](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568882853) fails its accepted-extras assertion on `3076188279c0ea657ec77aeeabebf1f82061eaaf`.
- The same assertion repeats in the [later main target](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678904598).
- The provider input is accepted far enough to continue, but the in-container parser does not emit the contract breadcrumb proving extra keys reached it.
- This is separate from the Slack `fast-uri` packaging failure in the same job.

## Description

The messaging provider E2E cannot prove that accepted extra fields survive transport into the in-container parser.

Expected: an accepted-extras input produces the documented, machine-checkable breadcrumb.

Actual: the target evaluates the breadcrumb predicate as false.

## Reproduction Steps

1. Run the Messaging providers Docker E2E against either candidate.
2. Exercise the accepted provider-extras fixture.
3. Observe the missing breadcrumb assertion.

## Environment

- GitHub Actions Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Debug Output

```text
accepted-extras breadcrumb proves extra keys reached in-container parser: expected false to be true
```

## Acceptance Criteria

- Define one stable parser-level signal for accepted extras.
- Product code and the E2E assertion use the same contract.
- The extras case and rejection cases both pass.

## Candidate Fix

- [PR #11011 — fix(messaging): load default runtime plan for extra placeholders](https://github.com/NVIDIA/NemoClaw/pull/11011), authored by @apurvvkumaria.
- Status at linkage: open and ready for review.
- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) still logs all three extra Telegram keys as ignored because the empty runtime-plan path did not fall back to the baked plan.
- #11011 owns the product/parser fix and retains both accepted and rejected key coverage. PR #10996 must not replace this proof with an environment-only assertion.
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
{"case_id": "NVIDIA_NemoClaw__10967__685eab2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
