# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Docs] Experimental NemoCUA reference omits local-Ollama unsupported restriction

## Description

The "Experimental NemoCUA" reference section documents `NEMOCLAW_CUA_ENABLED` and `NEMOCLAW_CUA_SANDBOX_IMAGE_REF`, but does not mention that onboarding a `nemocua` sandbox against the host-local Ollama provider is rejected. Onboarding fails with `Unsupported host-local inference application 'nemocua'` because the host-local inference routing allowlist only covers `openclaw`, `hermes`, and `langchain-deepagents-code`. A reader following the documented `NEMOCLAW_CUA_ENABLED` + `NEMOCLAW_CUA_SANDBOX_IMAGE_REF` steps with a local Ollama provider has no way to know this combination is unsupported until onboarding fails.

Platform scope: Not platform-specific — this is CLI/provider-routing behavior, not tied to host OS. Verified on Ubuntu 26.04 x86_64; other platforms not tested.
Regression: No — this restriction has been in place since NemoCUA moved to the current single-gate design; not a new regression.

## Environment

```text
Device:        x86_64 Linux VM
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Docker:        Present (container runtime), health: healthy
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (nemocua onboard did not reach Ready)
```

## Steps to Reproduce

1. Export the CUA gate:
   ```bash
   export NEMOCLAW_CUA_ENABLED=1
   export NEMOCLAW_CUA_SANDBOX_IMAGE_REF=<any syntactically valid image reference>
   export NEMOCLAW_PROVIDER=ollama
   ```
2. Attempt onboard:
   ```bash
   nemoclaw onboard --agent nemocua --name <sandbox> --non-interactive --yes
   ```
3. Compare against the "Experimental NemoCUA" reference section, which lists only the two env vars above with no provider restriction noted.

## Expected Result

Either the docs state up front that host-local Ollama is not a supported inference route for NemoCUA (so callers pick a supported provider before attempting onboard), or onboarding accepts the same host-local Ollama routing already supported for OpenClaw, Hermes, and LangChain Deep Agents Code.

## Actual Result

Onboarding fails and the docs give no advance warning:

```text
Error: Unsupported host-local inference application 'nemocua'.
```

## Logs

```text
nemoclaw onboard --agent nemocua --name <sandbox> --non-interactive --yes
...
Error: Unsupported host-local inference application 'nemocua'.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `77489fb04afc427879f6bc14ad07add2616b994c`.  There
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
{"case_id": "NVIDIA_NemoClaw__11057__77489fb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
