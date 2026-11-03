# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(googlechat): checked-in provider profile no longer matches credential boundary

## Investigation Summary

- [OpenClaw channels stop/start](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568886730) fails when adding Google Chat on `3076188279c0ea657ec77aeeabebf1f82061eaaf`.
- The same profile-boundary mismatch repeats on [later main](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678908449).
- The checked-in `google-chat-bridge` provider profile does not match NemoClaw's checked-in `googlechat` credential boundary.
- The stricter profile-refresh behavior landed through [PR #10884](https://github.com/NVIDIA/NemoClaw/pull/10884).
- Related prior lifecycle issue #10660 is closed, but this is an earlier deterministic fixture/profile mismatch rather than the prior missing-binding symptom.

## Description

The OpenClaw and Hermes all-channel lifecycle targets cannot reach stop/start because Google Chat registration fails strict profile validation.

Expected: checked-in provider profiles and credential boundaries are generated or validated as one compatible contract.

Actual: main contains mutually incompatible checked-in definitions.

## Reproduction Steps

1. Run either the OpenClaw or Hermes channels stop/start Docker E2E.
2. Add the Google Chat channel.
3. Observe strict provider-profile validation fail before lifecycle assertions.

## Environment

- GitHub Actions Docker E2E
- Runs: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977), [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Debug Output

```text
OpenShell provider profile 'google-chat-bridge' does not match NemoClaw's checked-in googlechat credential boundary.
```

## Acceptance Criteria

- Regenerate or update the profile and credential boundary from a single source of truth.
- Add a static parity check that fails before live E2E.
- Both full channel stop/start targets pass.

## Latest Evidence

- The exact-candidate [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) reproduces the channel-lifecycle failure for both [OpenClaw](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163751543) and [Hermes](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163751050).
- The Hermes target progressed past the managed restart failure fixed by #11071 before reaching this provider-profile boundary.
- This issue now owns the shared Google Chat fixture/profile mismatch for both supported agents.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d7ad11fc64e0066057b958cbc5206b34727ea980`.  There
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
{"case_id": "NVIDIA_NemoClaw__10971__d7ad11f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
