# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][Onboard] NVIDIA Endpoints validation returns HTTP 404 for bundled Nemotron model

## Description
NemoClaw v0.0.117 non-interactive onboarding with the bundled NVIDIA Endpoints model `nvidia/nemotron-3-super-120b-a12b` fails provider validation with Chat Completions API HTTP 404. The same signature reproduced on multiple platforms before sandbox-specific assertions could run.

Platform scope: reproduced on Ubuntu 24.04, Jetson Thor, and WSL2 x86 runners. Other platforms were not tested for this exact provider-validation failure.

Regression: Unknown.

OpenShell issue: No. The failure occurs during NemoClaw onboarding provider validation before the target sandbox assertions run.

Docs contract: the `Understand Provider Validation` documentation says NemoClaw validates the selected NVIDIA Endpoints provider and model before sandbox creation, using `/v1/chat/completions` and retrying transient upstream failures before reporting provider failure. The `Use NVIDIA Endpoints` documentation lists `nvidia/nemotron-3-super-120b-a12b` as a bundled fallback model.

## Environment
```text
Device:        Multi-platform test runners
OS:            Ubuntu 24.04, Jetson Thor, WSL2 x86
Architecture:  x86_64 and aarch64 coverage represented
Node.js:       v22.22.3 observed on Ubuntu 24.04
npm:           10.9.8 observed on Ubuntu 24.04
Docker:        docker runtime available
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
OpenClaw:      2026.7.1 where onboarding completed far enough to install agent assets
Provider:      build / nvidia-prod
Model:         nvidia/nemotron-3-super-120b-a12b
```

## Steps to Reproduce
1. Install NemoClaw v0.0.117 on a supported runner.
2. Start non-interactive onboarding for an OpenClaw or Hermes sandbox with provider `build`, NVIDIA Endpoints credentials, no GPU, and model `nvidia/nemotron-3-super-120b-a12b`.
3. Let onboarding reach `Configuring inference provider`.

## Expected Result
NVIDIA Endpoints validation succeeds for the bundled fallback model, or failures are limited to clearly actionable credential or endpoint errors after retrying transient upstream failures.

## Actual Result
Onboarding stops during provider validation and prints `NVIDIA Endpoints endpoint validation failed`. The validation probe summary reports `Chat Completions API: HTTP 404`. Downstream test assertions are skipped because setup never completes.

## Logs
```text
Representative onboarding excerpt:
[3/8] Configuring inference provider
[non-interactive] Provider: build
NVIDIA Endpoints endpoint validation failed.
Validation probe summary: Chat Completions API: HTTP 404.
Validation details were omitted to avoid exposing credentials.

The same Chat Completions API HTTP 404 validation signature reproduced on Ubuntu 24.04, Jetson Thor, and WSL2 x86 reruns.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5b74336486a8492ad87dd7eaba3d1bc06abbadf6`.  There
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
{"case_id": "NVIDIA_NemoClaw__10880__5b74336",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
