# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(security): transient hosted-inference outage fails OpenClaw posture qualification

## Investigation Summary

- [Security: OpenClaw](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568886810) fails its hosted inference turn on `3076188279c0ea657ec77aeeabebf1f82061eaaf` with a LiteLLM `ServiceUnavailableError`.
- The provider failure leaves no assistant message/session evidence, causing the posture target to fail downstream assertions.
- The [same target passes](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678908706) on later main candidate `eb3fa2e5097389d7dd8e2643552788ff16d8f14a`.
- This is classified as an external/provider transient; the issue is E2E resilience and failure classification rather than a confirmed security-posture regression.

## Description

A temporary hosted inference outage makes the entire OpenClaw security posture target red even when its local security checks may be healthy.

Expected: provider-dependent proof has bounded retry/failover and clearly distinguishes provider availability from security posture failure.

Actual: one transient `ServiceUnavailableError` produces empty turn evidence and a generic red security target.

## Reproduction Steps

1. Run Security: OpenClaw with NVIDIA hosted inference.
2. Cause or encounter a temporary provider 5xx/unavailable response during the required turn.
3. Observe missing assistant/session evidence fail the target.

## Environment

- GitHub Actions Docker E2E
- NVIDIA hosted inference
- Failed run: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977)
- Passing comparison: [33761515943](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943)

## Acceptance Criteria

- Add bounded retry or approved fallback for transient provider availability failures.
- Preserve fail-closed behavior for invalid security posture or invalid responses.
- Report provider-outage classification separately from posture assertions.
- Demonstrate repeated target passes or an explicit infrastructure conclusion.

## Candidate Fix

- [PR #11077 — fix(e2e): retry transient OpenClaw provider turns](https://github.com/NVIDIA/NemoClaw/pull/11077), authored by @cjagwani.
- Status at linkage: open draft.
- The PR adds one bounded retry only for positively classified transient provider unavailability, while authentication, policy, invalid-response, and unknown failures remain fail-closed.
- Keep this issue open until the PR is rebased on current main and the security target passes repeatedly.

## Latest Evidence

- [Hosted inference in exact-candidate run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163751707) failed during initial deployment verification because dashboard port 18789 refused connections. That earlier failure is tracked in #11084.
- The run did not reach this issue's hosted-inference outage classification. PR #11077 remains the candidate for the original failure, but this exact run neither confirms nor disproves it.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b98c869ab27a44039aeee6f535b2b0b1ff6d4499`.  There
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
{"case_id": "NVIDIA_NemoClaw__10978__b98c869",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
