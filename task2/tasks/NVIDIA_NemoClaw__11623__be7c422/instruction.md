# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Install][Channel] Google Chat onboarding times out after duplicate refresh configuration

## Investigation Summary

- Reproduced during a fresh local-source installation on Ubuntu 24.04.4 with OpenShell 0.0.116. The first Google Chat token mint succeeds; sandbox creation configures the same refresh again and times out at `configured`.
- Retained gateway state shows the second configuration kept the existing token expiry and scheduled the next refresh about 55 minutes after the first mint.
- A local patch on `01ac06bb68d90621f517c996fe4eda754aebf7a6` completes onboarding with one refresh configuration, and the user confirmed a Google Chat reply. Its 10 focused unit tests and CLI typecheck passed.
- Scope: reuse a confirmed refresh registration within one onboarding process. Recovery of an already-failed session in a new process remains separate.

## Description

Google Chat onboarding registers credentials before sandbox creation so an interrupted install can resume. The create phase applies the provider again. When the provider already matches, the messaging applier preserves it but still calls `configureProviderRefresh`.

OpenShell resets refresh status to `configured` while retaining the existing expiry. Its worker waits until the scheduled refresh, but NemoClaw expects a new mint within its bounded polling window. Onboarding fails before a sandbox is created despite the successful first mint.

Expected: the create phase reuses the successful registration when the gateway, refresh inputs, and provider revision still match. It must still observe readiness. Changed credentials, scopes, or provider identity must invalidate reuse; failed or unconfirmed minting must remain an error.

The fix must also account for OpenShell publishing `refreshed` before writing the token to the provider. A reusable receipt must wait for the provider update. The deterministic regression exercises that ordering on every run.

The behavior belongs in the shared messaging applier, following the manifest-first architecture. Source review identifies the provider-reuse change in #11009 as the regression boundary; this has not been live-bisected against the preceding revision.

## Reproduction Steps

1. Start with a clean environment and the affected NemoClaw source revision `21a363701a3e9129722f03b74580928bd09ad8af`. Install from that checkout:

   ```bash
   NEMOCLAW_REPO_ROOT="$(pwd)" bash install.sh
   ```

2. Select OpenClaw, NVIDIA Endpoints, and the default Nemotron 3 Super model.
3. Enable Google Chat and complete the webhook URL, valid service-account, and sender setup. Keep the default resource settings.
4. Observe credential staging mint a token successfully, then sandbox creation configure refresh again and fail with `last status 'configured'`.

## Environment

- Ubuntu 24.04.4 LTS, x86_64, Docker Engine 29.8.0.
- Node.js 22.23.2; npm 10.9.8.
- Failing NemoClaw build: `v0.0.123-47-g21a363701`.
- OpenShell CLI/gateway: 0.0.116.
- Agent/channel: OpenClaw with Google Chat.
- Inference: NVIDIA Endpoints, `nvidia/nemotron-3-super-120b-a12b`.

## Debug Output

The failed installation was replaced before a debug bundle was collected. The retained, redacted gateway and onboarding-session observations below are from 2026-09-12; times are UTC.

```text
Messaging credential staging completed: 05:00:10.581
Onboarding failed:                     05:03:14.985
Gateway inspected:                     05:05:35
Refresh STATUS:                        configured
LAST_REFRESH:                          05:00:10
EXPIRES_AT:                            06:00:09
NEXT_REFRESH:                          05:55:09
Gateway service:                       active/running
Sandbox count:                         0
```

Validation of the local patch: the user repeated the local-source install, the log contains one `Configured refresh` entry, installation completed, and the bot replied. The focused test file passed 10/10 cases. CLI typecheck passed with an 8 GiB Node heap after the default heap exhausted memory. The patch is not yet published.

## Logs

Relevant excerpts, with intervening output omitted:

```text
Configured refresh for my-assistant-googlechat-bridge GOOGLE_CHAT_ACCESS_TOKEN
Waiting for the gateway to mint GOOGLE_CHAT_ACCESS_TOKEN.
Registered selected credentials with OpenShell for resume.

[6/8] Creating sandbox
Configured refresh for my-assistant-googlechat-bridge GOOGLE_CHAT_ACCESS_TOKEN
Waiting for the gateway to mint GOOGLE_CHAT_ACCESS_TOKEN.
Error: Gateway token <REDACTED> did not complete for messaging provider 'my-assistant-googlechat-bridge' (last status 'configured').
```

Related: #11186 concerns a credential-free E2E fixture bypass during rebuild. This report concerns real service-account minting during fresh onboarding.

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `be7c422f136d6688b258540804120e54799e05e8`.  There
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
{"case_id": "NVIDIA_NemoClaw__11623__be7c422",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
