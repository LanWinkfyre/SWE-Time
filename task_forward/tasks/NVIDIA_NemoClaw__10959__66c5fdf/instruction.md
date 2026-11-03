# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Sandbox] Sandbox rebuild still fails with N1x validation pending preflight after PR #9312 fix (v0.0.119)

## Description

Follow-up to #9292 (closed). The original fix (PR #9312) does not resolve the issue — the bug is still reproducible on NemoClaw v0.0.119.

After a successful N1x Express preview install with managed vLLM, adding a messaging channel (e.g. Slack) via `nemoclaw my-assistant channels add slack` triggers a sandbox rebuild. The rebuild fails at onboard runtime preflight with "N1x platform validation is pending a physical NemoClaw Express E2E run." The Express install flow waives `host.platform.n1x_validation_pending` when the user accepts the Deferred preview prompt, but the rebuild path re-runs the onboard runtime preflight without carrying the waiver forward.

The sandbox is left untouched (no data loss), but the user cannot apply any configuration change that requires a rebuild (channels, policy presets, etc.) on an N1x Express install.

Platform scope: Reproduced on N1x Linux only; other platforms not tested.
Regression: No — N1x Express is new functionality; this has never worked through rebuild.
OpenShell issue: No

## Environment

```text
Device:        N1x Linux Laptop (RTX Spark N1X, aarch64, 61 GiB unified RAM)
OS:            Ubuntu 24.04 (aarch64)
NemoClaw:      v0.0.119
```

## Steps to Reproduce

1. On N1x Linux Laptop, install NemoClaw v0.0.119 via Express:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash
   ```
2. Accept the Deferred N1x preview prompt (Y) when shown.
3. Wait for Express install to complete (sandbox created, vLLM healthy).
4. Add a messaging channel:
   ```bash
   nemoclaw my-assistant channels add slack
   ```
5. Enter valid Slack tokens and member/channel IDs.
6. When prompted "Rebuild my-assistant now to apply? [Y/n]:", choose Y.

## Expected Result

Rebuild succeeds. The N1x validation waiver granted during Express install carries forward to subsequent rebuild operations.

## Actual Result

Rebuild fails at onboard runtime preflight:

```text
Rebuild sandbox my-assistant
  Current:  OpenClaw v2026.7.1
  Target:   OpenClaw v2026.7.1

N1x platform validation is pending a physical NemoClaw Express E2E run.

Rebuild preflight failed: the replacement onboarding host/runtime checks did not pass.
onboard runtime preflight exited with code 1
Aborting rebuild -- sandbox is untouched, no data was lost.
Replacement onboarding preflight failed
```

## Logs

```text
nvidia@localhost:~$ nemoclaw my-assistant channels add slack
  Effective egress that would be opened:
    policy 'slack':
      - slack.com:443 (protocol: rest, enforcement: enforce)

  ... (channel configuration accepted) ...

  Rebuild sandbox my-assistant
    Current:  OpenClaw v2026.7.1
    Target:   OpenClaw v2026.7.1

  N1x platform validation is pending a physical NemoClaw Express E2E run.

  Rebuild preflight failed: the replacement onboarding host/runtime checks did not pass.
  onboard runtime preflight exited with code 1
  Aborting rebuild -- sandbox is untouched, no data was lost.
  Replacement onboarding preflight failed
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `66c5fdfe98cbb783bd80938adf209e34ad5e8bdc`.  There
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
{"case_id": "NVIDIA_NemoClaw__10959__66c5fdf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
