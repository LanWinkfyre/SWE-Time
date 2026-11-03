# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Onboard] onboard --fresh fails with "inference route reservation belongs to another onboarding session" while priming an Ollama model, even from a clean single-attempt run

## Description

Running `nemoclaw onboard --name {sandbox} --fresh` through the system-installed-Ollama provider path fails during the "Priming Ollama model" step with "Cannot replace sandbox '{sandbox}': its inference route reservation belongs to another onboarding session." This happens even when the prior attempt for the same sandbox name was fully destroyed and no other onboarding process was running at the time.

Platform scope: Reproduced on Ubuntu 24.04 x86_64 only; other platforms not tested.
Regression: Unknown — earlier versions not tested for this specific flow.
OpenShell issue: No — the failure and message are emitted by the NemoClaw `onboard` command.

## Environment

```text
Device:        Linux server (Docker container runtime)
OS:            Ubuntu 24.04 LTS
Architecture:  x86_64
Node.js:       Not captured
npm:           Not captured
Docker:        29.7.2 (server)
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (onboard did not complete)
```

## Steps to Reproduce

1. Ensure no prior sandbox of this name exists:
   ```bash
   nemoclaw {sandbox} destroy --yes
   ```
2. Clear any stale lock:
   ```bash
   rm -f ~/.nemoclaw/gateways/{port}/onboard.lock
   ```
3. Confirm no nemoclaw-related node process is running:
   ```bash
   pgrep -f nemoclaw
   ```
4. Run onboarding:
   ```bash
   export NEMOCLAW_GATEWAY_PORT={port}
   export NEMOCLAW_OLLAMA_INSTALL_MODE=system
   export NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1
   nemoclaw onboard --name {sandbox} --fresh
   ```
5. At the interactive prompts, select the default agent, then select "Local Ollama" / "Install Ollama (Linux)" as the inference provider, select the offered starter model, confirm the download, accept the default "Apply configuration" action.
6. Observe the "[4/8] Setting up inference provider" step through "Priming Ollama model: {model}".

## Expected Result

Onboarding proceeds past the "Priming Ollama model" step and completes sandbox creation, since this is a single onboarding session with no other onboarding process running against the same sandbox name.

## Actual Result

Onboarding fails at the priming step with:

```text
Error: Cannot replace sandbox '{sandbox}': its inference route reservation belongs to another onboarding session
```

Reproduced twice in a row, each time starting from a verified-clean state (sandbox destroyed, stale onboard.lock removed, no other nemoclaw-related process running before the attempt). Both attempts failed at the identical step with the identical message.

## Logs

```text
  [4/8] Setting up inference provider
  ──────────────────────────────────────────────────
  ✓ Updated provider ollama-local
  Inference configured:

    Workspace: default
    Route:     inference.local
    Provider:  ollama-local
    Model:     qwen3.5:9b
    Version:   4
    Timeout:   180s
  Priming Ollama model: qwen3.5:9b
  Error: Cannot replace sandbox 'ollama-mode': its inference route reservation belongs to another onboarding session

  Onboarding did not finish. Resume from the step that failed with:
    nemoclaw onboard --resume
  Completed steps are skipped; pass --fresh instead to start over.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a4e0605f64713e1056b934b47b13a87cc6a49c99`.  There
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
{"case_id": "NVIDIA_NemoClaw__11051__a4e0605",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
