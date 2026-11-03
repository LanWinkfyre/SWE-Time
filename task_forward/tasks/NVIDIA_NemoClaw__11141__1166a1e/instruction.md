# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Onboard] Gemini provider validation fails with Chat Completions HTTP 400 during non-interactive Hermes onboarding

## Description

Non-interactive NemoHermes onboarding with the Gemini provider can fail during live provider validation before any sandbox is created. The local Docker Desktop / WSL environment and OpenShell gateway preflight are healthy, but the Gemini Chat Completions validation probe returns HTTP 400 and onboarding aborts.

Platform scope: WSL2 ARM with Docker Desktop runtime.

Regression: Unknown — earlier releases were not isolated for this exact HTTP 400 validation path in this session.

OpenShell issue: No — the OpenShell gateway preflight is healthy before provider validation fails.

## Environment

```text
OS: WSL2 Linux
Architecture: ARM64
NemoClaw release: v0.0.120
Agent/runtime: NemoHermes
Provider: Google Gemini
Model: gemini-2.5-flash
Execution mode: non-interactive onboarding
Docker runtime: Docker Desktop integration
```

## Steps to Reproduce

1. Start from a clean WSL2 runner environment with Docker Desktop integration enabled.
2. Run non-interactive NemoHermes onboarding using the Gemini provider and a configured Gemini API key.
3. Observe provider validation during the onboarding provider-configuration phase.

## Expected Result

The Gemini provider validation should either succeed with the configured model, or return an actionable validation error that identifies a real credential, model, or configuration issue.

## Actual Result

Preflight passes and the Docker-driver gateway becomes healthy. During provider configuration, onboarding fails with:

```text
Google Gemini endpoint validation failed.
Validation probe summary: Chat Completions API: HTTP 400.
```

Validation details were omitted to avoid exposing credentials. Onboarding aborts before sandbox creation and releases the managed gateway.

## Impact

Gemini-backed NemoHermes onboarding cannot proceed on the affected WSL2 ARM path, so Gemini tool-schema sanity coverage cannot obtain a trustworthy pass/fail result.

## Related Issues

A related Gemini validation issue exists for a different response-shape symptom, but this report is for the HTTP 400 validation response during onboarding.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1166a1eee447936cbf97459056fa042657fe6cee`.  There
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
{"case_id": "NVIDIA_NemoClaw__11141__1166a1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
