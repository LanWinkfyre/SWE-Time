# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Inference] inference set missing-provider error does not provide gateway-scoped selectable suggestions

## Description

When nemoclaw inference set is given a provider name that is not registered, the error
prints a fixed "Supported providers" list of provider adapter type names. The list is
emitted without consulting the target gateway, so it is not scoped to the providers that
are actually registered and selectable there.

On the host used here the gateway had exactly three registered providers, but the
guidance named twelve, nine of which cannot be selected on that gateway at all. A user
who follows the suggestion gets a second failure.

The same list is printed byte for byte for two different unregistered provider names,
which shows it is static rather than derived from gateway state.

What the command does correctly: it exits non-zero, it does not name a registered
non-inference provider that was added for this test, it exposes no credential value, and
the invalid request does not change the existing route.

Platform scope: Reproduced on Ubuntu 26.04 x86_64 only; other platforms not tested.
Regression: Unknown - earlier versions not tested for this path.
OpenShell issue: No

## Environment

```text
Device:        Ubuntu 26.04 host, x86_64
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Node.js:       v22.23.2
npm:           Not on PATH (installer-managed Node.js)
Docker:        Docker version 29.7.2, build a7dcaa6
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.121
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. Confirm what is actually registered on the gateway:

     nemoclaw credentials list

   On this host it listed exactly three: nvidia-prod, compatible-endpoint, ollama-local.

2. Onboard a disposable sandbox, for example:

     NEMOCLAW_PROVIDER=ollama NEMOCLAW_MODEL=qwen2.5:1.5b nemoclaw onboard \
       --name provider-sugg --no-gpu --non-interactive --yes

3. Ask for a provider that is not registered:

     nemoclaw inference set --provider provider-not-registered \
       --model model-not-registered --sandbox provider-sugg

4. Repeat with a different unregistered provider name:

     nemoclaw inference set --provider other-provider-not-registered \
       --model model-not-registered --sandbox provider-sugg

5. Confirm the route was not changed:

     nemoclaw inference get
```

## Expected Result

The error names providers the user can actually select on this gateway, so acting on the
suggestion succeeds instead of producing a second failure.

## Actual Result

Step 3, verbatim:

  Unsupported provider 'provider-not-registered'. Supported providers: nvidia-prod,
  nvidia-nim, nvidia-router, openai-api, openrouter-api, anthropic-prod,
  compatible-anthropic-endpoint, gemini-api, compatible-endpoint, hermes-provider,
  ollama-local, vllm-local.

  exit code 2

Step 4, verbatim, with a different invalid provider name:

  Unsupported provider 'other-provider-not-registered'. Supported providers: nvidia-prod,
  nvidia-nim, nvidia-router, openai-api, openrouter-api, anthropic-prod,
  compatible-anthropic-endpoint, gemini-api, compatible-endpoint, hermes-provider,
  ollama-local, vllm-local.

  exit code 2

The suggestion list is identical in both cases.

Of the twelve names printed, only nvidia-prod, compatible-endpoint and ollama-local are
registered on this gateway per step 1. The other nine - nvidia-nim, nvidia-router,
openai-api, openrouter-api, anthropic-prod, compatible-anthropic-endpoint, gemini-api,
hermes-provider, vllm-local - are not selectable here.

Step 5 confirmed the route was unchanged after both failed attempts.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `475a20e00db5984d026b70d0a01654a2822b6a7a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11413__475a20e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
