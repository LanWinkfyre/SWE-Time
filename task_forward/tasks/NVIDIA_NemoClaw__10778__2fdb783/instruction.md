# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Hermes Portable Ollama onboard fails with gateway mutation authority changed even on a fresh onboard

## Description

Fresh (non-resumed, `--fresh`) onboarding of a Hermes agent under the Experimental Portable profile with the `ollama-local` provider consistently fails during inference provider setup with "Hermes Portable inference gateway mutation authority changed." This happens even with a fully cleared onboarding session, gateway state directory, and portable-inference authority cache — it is not resolved by starting from a genuinely clean state.

Platform scope: Reproduced on Ubuntu 25.04 only; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No — root cause traced to NemoClaw's own host-local inference routing and Hermes Portable gateway transaction code, not the OpenShell CLI/runtime.

## Environment

```text
Device:        Ubuntu x86_64 server with NVIDIA GPU (A100 40GB)
OS:            Ubuntu 25.04
Architecture:  x86_64
Node.js:       v22.16.0
Docker:        29.5.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
OpenClaw:      N/A (onboard never reached Ready)
```

## Steps to Reproduce

1. On a host with rootless Podman and an NVIDIA GPU, ensure no prior onboarding session/journal/authority cache exists for the target sandbox name (clear `~/.nemoclaw/gateways/{port}/onboard-session.json`, `~/.nemoclaw/portable-inference/`, and `~/.nemoclaw/launch-readiness/` if retrying).
2. Run:
   ```bash
   nemoclaw onboard --experimental-profile portable --agent hermes --name {sandbox} --fresh --yes
   ```
   with `NEMOCLAW_NON_INTERACTIVE=1` and `NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1` set.
3. Let the wizard auto-select the `ollama-local` provider (no API key provided) and confirm the model shown at the "Review configuration" screen.
4. Observe the onboarding proceed through preflight, gateway startup, and into "[4/8] Setting up inference provider."
5. Observe that a portable Ollama container is created and starts successfully (confirm with `podman ps -a` — a `nemoclaw-portable-ollama-*` container reaches "Up", and an ephemeral `nemoclaw-inference-probe-*` container exits 0, proving the model responds correctly over the network).
6. Observe onboarding then fail immediately after with "Hermes Portable inference gateway mutation authority changed."

## Expected Result

Onboarding should proceed to register the working Ollama route with the OpenShell gateway and continue to sandbox creation, since the underlying Ollama runtime is already confirmed healthy and reachable (per the exit-0 inference probe in step 5). Per the documented design, the portable host-local endpoint should be addressed via `host.openshell.internal` (the OpenShell Podman host gateway mapping).

## Actual Result

Onboarding aborts with "Hermes Portable inference gateway mutation authority changed," even though this is a genuinely fresh attempt (fresh onboarding session, fresh gateway, fresh sandbox name, no reused state) and the underlying Ollama runtime is confirmed healthy. Reproduced identically across multiple fully-cleared fresh attempts.

Code-level cause: `prepareGatewayMutation` in the Hermes Portable gateway transaction code hardcodes an expected provider base URL of exactly `http://host.openshell.internal:11434/v1`. The actual base URL passed at mutation time is constructed dynamically as `http://${receipt.endpoint.host}:${port}/v1` from the host-local inference routing code, which only normalizes `endpoint.host` to the `host.openshell.internal` constant under a separate, apparently non-firing condition for this Portable Hermes code path — leaving the receipt's real (concrete IP) host value, which then never equals the hardcoded expectation and trips the "authority changed" guard on every attempt.

## Logs

```text
[3/8] Configuring inference provider
──────────────────────────────────────────────────
Review configuration
──────────────────────────────────────────────────
Provider:      ollama-local
Model:         qwen3-vl:4b
Sandbox name:  hermes-probe-test
──────────────────────────────────────────────────
[4/8] Setting up inference provider
──────────────────────────────────────────────────
Host-local inference failure [runtime provider 'podman']: Hermes Portable inference gateway mutation authority changed.

Onboarding did not finish. Resume from the step that failed with:
  nemoclaw onboard --resume
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2fdb783533f58c7e316aedf7595a1808c9589bbc`.  There
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
{"case_id": "NVIDIA_NemoClaw__10778__2fdb783",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
