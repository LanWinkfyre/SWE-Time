# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Onboard] N1x has no non-Express install path — declining the Express preview exits the installer

## Description

On N1x Linux, declining the Deferred N1x Express preview prompt (answering `n`) does not fall back to the ordinary interactive onboarding wizard the way every other platform does. Instead the installer immediately hard-exits with an error, so there is no way to reach the interactive provider-selection step and choose a non-vLLM provider (e.g. a locally installed Ollama) on N1x.

Platform scope: Reproduced on N1x Linux only. On other platforms, declining the equivalent express-install prompt continues into the ordinary interactive onboarding flow instead of exiting.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        N1x Linux Laptop (RTX Spark N1X, aarch64)
OS:            Ubuntu 24.04.4 LTS (aarch64)
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        server 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (install exited before onboarding started)
```

## Steps to Reproduce

1. On N1x Linux, run:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash
   ```
2. At "Type 'yes' to accept the NemoClaw license and third-party software notice and continue [no]:", type `yes`
3. At "Run the Deferred N1x preview with these settings? [Y/n]:", type `n`

## Expected Result

Declining the Express preview should continue into the ordinary interactive onboarding wizard, the same way declining the equivalent express prompt behaves on other platforms, letting the user choose a different inference provider (for example a locally installed Ollama instance).

## Actual Result

```text
[ERROR] N1x onboarding currently requires the Deferred managed-vLLM preview. Re-run the installer and accept the preview, or set NEMOCLAW_PROVIDER=install-vllm.
```

The installer exits immediately. There is no way to reach interactive provider selection on N1x — the only path forward is accepting the vLLM Express preview or explicitly forcing `NEMOCLAW_PROVIDER=install-vllm`, both of which route through vLLM specifically. A user who already has a local Ollama instance set up has no way to use it on N1x.

## Logs

```text
nvidia@localhost:~$ curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash

  Launch OpenClaw in an OpenShell sandbox.  v0.0.119

[INFO]  Installer stdin is piped; prompting for the third-party software notice on /dev/tty before install.

  Third-Party Software Notice - NemoClaw Installer
  ...
  Type 'yes' to accept the NemoClaw license and third-party software notice and continue [no]: yes
[INFO]  Detected N1x.
  The Deferred N1x preview will configure managed local vLLM with Qwen3.6 35B-A3B NVFP4.
  N1x Express is a Deferred preview pending a physical NemoClaw Express E2E run; accepting this prompt is explicit preview intent, not a supported-platform claim. The N1x profile uses one host and does not activate DGX Spark cluster discovery or fixed catalog behavior. Managed vLLM pulls the pinned image and model only after the existing CUDA and CDI readiness checks pass.
  Sandbox name: my-assistant.
  It runs onboarding non-interactively, but still prompts for sudo when host setup needs it.
  Sandbox policy: suggested mode, tier 'balanced'. This uses the base sandbox policy plus npm, pypi, huggingface, brew, and the selected web-search preset, and local-inference access when needed.
  Run the Deferred N1x preview with these settings? [Y/n]: n
[ERROR] N1x onboarding currently requires the Deferred managed-vLLM preview. Re-run the installer and accept the preview, or set NEMOCLAW_PROVIDER=install-vllm.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `94bb868ea0f3e98533b06196def74b7559a1d1d4`.  There
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
{"case_id": "NVIDIA_NemoClaw__11041__94bb868",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
