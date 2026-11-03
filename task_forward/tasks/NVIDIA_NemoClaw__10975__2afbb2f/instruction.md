# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(brev): exact-staging target receives an invalid NVIDIA credential shape

## Investigation Summary

- [Exact staging Brev Launchable](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977/job/100568884177) passes boot, provenance, and systemd validation on candidate `3076188279c0ea657ec77aeeabebf1f82061eaaf`.
- It stops before provider selection because the injected NVIDIA credential does not begin with the required `nvapi-` prefix.
- The target was [skipped in the later main run](https://github.com/NVIDIA/NemoClaw/actions/runs/33761515943/job/100678905989), so there is no clean rerun proving the staging secret was repaired.
- No secret value is included in this report.

## Description

The exact-staging environment supplies the wrong credential type/value to the NVIDIA inference E2E.

Expected: the environment secret referenced by this target is an NVIDIA API key with the validated `nvapi-` shape.

Actual: validation rejects the credential before inference-provider qualification begins.

## Reproduction Steps

1. Dispatch the exact staging Brev Launchable target with its configured environment.
2. Allow boot/provenance/systemd checks to complete.
3. Observe provider credential validation fail before provider selection.

## Environment

- GitHub Actions environment-backed secret
- Brev exact staging
- Run: [33730208977](https://github.com/NVIDIA/NemoClaw/actions/runs/33730208977)

## Debug Output

```text
Invalid NVIDIA API key. Must start with nvapi-.
```

## Acceptance Criteria

- Correct the environment secret reference or secret value without exposing it.
- Add a pre-dispatch credential-shape check that identifies the secret/environment name, never its value.
- Rerun exact staging successfully on the current main candidate.

## Resolution

- [PR #11022 — fix(e2e): preserve hosted inference for Brev](https://github.com/NVIDIA/NemoClaw/pull/11022), authored by @jyaunches, merged on 2026-09-04 and closed this issue.
- The PR repairs the environment credential handoff without exposing the credential value.
- The exact-staging jobs were skipped in run 33915961523, so the next full main run still needs to supply the final staging qualification evidence tracked by #10979.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2afbb2f09128d9cc90711b5a37076431a932d82e`.  There
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
{"case_id": "NVIDIA_NemoClaw__10975__2afbb2f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
