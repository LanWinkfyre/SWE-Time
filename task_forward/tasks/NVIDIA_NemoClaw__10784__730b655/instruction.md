# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Inference] inference get never reports the endpoint URL in either output form, but inference set requires --endpoint-url for custom compatible routes

## Description

`nemoclaw {sandbox} inference get` never reports the endpoint URL the sandbox was onboarded against, in either output form. Both the plain and the `--json` output carry only the provider and the model.

At the same time, `nemoclaw {sandbox} inference set` for a custom compatible provider requires `--endpoint-url`, and refuses without it. The documented reason is sound - a custom compatible route has to prove endpoint and API-family compatibility against every other sandbox on the same gateway - but the value it demands cannot be read back from the product, so the round trip is broken. An operator or script that wants to change only the model on an existing compatible sandbox has no supported way to recover the URL that sandbox is already bound to.

Platform scope: Reproduced on a DGX Spark aarch64 and an Ubuntu 24.04 x86_64 host, on both a custom compatible-endpoint sandbox and an unrelated cloud-provider sandbox; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        DGX Spark, and separately an Ubuntu 24.04 x86_64 host
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64 and x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.2.1, build a5c7197
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. Onboard a sandbox against a local OpenAI-compatible endpoint, for example a disposable server on
   127.0.0.1:8000 that answers /v1/models and /v1/chat/completions:

   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=custom \
     NEMOCLAW_ENDPOINT_URL=http://127.0.0.1:8000/v1 NEMOCLAW_MODEL=test-model \
     NEMOCLAW_COMPATIBLE_AUTH_MODE=none NEMOCLAW_PROVIDER_KEY=none \
     nemoclaw onboard --fresh --non-interactive --no-gpu --name lb694p --yes \
     --yes-i-accept-third-party-software

2. Read the route back in both forms:
   nemoclaw lb694p inference get
   nemoclaw lb694p inference get --json

3. Try to change only the model, without repeating the URL:
   nemoclaw lb694p inference set --provider compatible-endpoint --model test-model \
     --inference-api openai-completions
```

## Expected Result

Step 2 reports the endpoint URL the sandbox is bound to, so step 3 can supply it, or step 3 reuses the
recorded URL when it is not given. Either way the value the command requires is obtainable from the
product.

## Actual Result

```text
Step 2, plain form, on a compatible-endpoint sandbox:

  Provider: compatible-endpoint
  Model:    test-model

Step 2, JSON form, on the same sandbox - the object has exactly two keys:

  {
    "provider": "compatible-endpoint",
    "model": "test-model"
  }

Step 3 then refuses:

  endpoint-url is required for custom-compatible metadata.
  [exit=2]

Supplying the URL explicitly works, which confirms nothing else is wrong with the route:

  nemoclaw lb694p inference set --provider compatible-endpoint \
    --endpoint-url http://127.0.0.1:8000/v1 --model test-model --inference-api openai-completions
    Setting OpenShell inference route: compatible-endpoint / test-model
    Context window for 'test-model': 131072 tokens
    Inference route synced for 'lb694p': inference/test-model
  [exit=0]
```

## Logs

```text
The same omission on an unrelated healthy sandbox using a hosted provider, so it is not specific to
the compatible-endpoint path:

  nemoclaw my-assistant inference get
    Provider: nvidia-prod
    Model:    nvidia/nemotron-3-super-120b-a12b
  lines mentioning endpoint or url or http: 0

  nemoclaw my-assistant inference get --json
    parsed keys: ['model', 'provider']

The sandbox-scoped status output does not carry it either: `status --json` reports `recordedRoute`
and `liveRoute` as provider and model only.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `730b6550558460081458fa83d5b1ad937428d05a`.  There
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
{"case_id": "NVIDIA_NemoClaw__10784__730b655",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
