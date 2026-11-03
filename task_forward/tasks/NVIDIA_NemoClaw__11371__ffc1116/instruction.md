# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][CLI&UX] nemoclaw {sandbox} agent -m takes 4-7 minutes to dispatch on an idle Ready sandbox

## Description

A one-shot `nemoclaw {sandbox} agent -m "..."` request against a healthy, idle, Ready sandbox takes 4-7 minutes of dead time before the request is actually dispatched to the sandbox/gateway. Once dispatched, the entire round trip (gateway processing + model inference) completes in under 1 second. Confirmed twice independently on an idle host (load average ~0.3-2.3), no concurrent NemoClaw activity from this session at the time of either attempt.

Platform scope: Reproduced on Ubuntu 24.04 x86_64 only; other platforms not tested this round.
Regression: Unknown - earlier versions not tested.
OpenShell issue: No

## Environment

```
Device:        Generic x86_64 Ubuntu server, no GPU
OS:            Ubuntu 24.04.4 LTS
Architecture:  x86_64
Docker:        29.5.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.121
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. On a clean host, run `nemoclaw onboard --name {sandbox} --non-interactive --fresh --yes --no-gpu` with a valid `NVIDIA_INFERENCE_API_KEY` set; sandbox reaches Ready normally.
2. Run `nemoclaw {sandbox} status --json`; completes in about 4 seconds, reports healthy/Ready with `inferenceHealth.ok=true`.
3. Immediately run `nemoclaw {sandbox} agent --agent main -m "Reply with exactly: AUTHORITY_BOUND_OK"`.
4. Observe the command does not return for several minutes.

## Expected Result

The one-shot agent command should dispatch promptly (seconds, not minutes) on an idle, Ready sandbox with a healthy inference route.

## Actual Result

Attempt 1: sandbox container log shows the SSH relay channel for the actual agent dispatch did not open until about 4 minutes 12 seconds after the prior status check completed; once opened, gateway processed the request in 157ms and the model responded in 499ms.

Attempt 2, a fresh isolated repro on the same host: command issued at 03:35:20 UTC, the SSH relay channel for dispatch did not open until 03:42:03 UTC, 6 minutes 43 seconds later; once opened, the model responded in 480ms and the command completed immediately after.

Both attempts eventually succeed with exit 0 and a real model response - this is a dispatch-latency issue, not a hang or deadlock. Note the model's reply text in both cases was a generic greeting, not the literal requested string; that is a separate, lower-priority instruction-following observation, not the focus of this report.

## Logs

Container log excerpt, attempt 2 (sandbox `auth-bind-primary`):

```
03:35:20 - host-side process starts (confirmed alive via ps throughout the wait, never dead/zombied)
2026-09-10T03:42:03.041Z OCSF NET:OPEN ssh relay open channel_id=629024aa-24b6-409e-9dbe-46823d4d945d
2026-09-10T03:42:06.599Z OCSF NET:OPEN ALLOWED inference.local:443
2026-09-10T03:42:06.593+00:00 [model-fetch] start provider=inference model=nvidia/nemotron-3-super-120b-a12b
2026-09-10T03:42:07.076+00:00 [model-fetch] response status=200 elapsedMs=480
Command exited shortly after.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ffc1116ce6f176fa5da7844e7f4e26d38aef7a21`.  There
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
{"case_id": "NVIDIA_NemoClaw__11371__ffc1116",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
