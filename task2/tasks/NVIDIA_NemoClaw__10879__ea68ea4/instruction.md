# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 22.04][Inference] OpenClaw nvidia-prod sandboxes return HTTP 404 through inference.local after onboarding

## Description
Fresh OpenClaw sandboxes on Ubuntu 22.04 complete onboarding with provider `nvidia-prod` and model `nvidia/nemotron-3-super-120b-a12b`, but subsequent sandbox status checks report the in-sandbox inference route as unhealthy because the model-invocation probe returns HTTP 404. This reproduces across multiple sandbox lifecycle flows in NemoClaw v0.0.117.

Platform scope: reproduced on Ubuntu 22.04 x86_64. Other platforms were not tested for this exact HTTP 404 failure.

Regression: Unknown.

OpenShell issue: Unknown. The failing surface is the NemoClaw sandbox status inference route through the OpenShell gateway.

Docs contract: the `Verify the Sandbox Inference Route` documentation says the status Inference row sends an in-sandbox request through `inference.local` and reports healthy only when the selected API family returns a structurally valid result. It also says the route-reachability and upstream subprobes identify the failing hop.

## Environment
```text
Device:        Ubuntu 22.04 test runner
OS:            Ubuntu 22.04
Architecture:  x86_64
Node.js:       v22.22.3
npm:           10.9.8
Docker:        docker runtime available
OpenShell CLI: 0.0.106 using docker gateway
NemoClaw:      v0.0.117
OpenClaw:      2026.7.1
Provider:      nvidia-prod
Model:         nvidia/nemotron-3-super-120b-a12b
```

## Steps to Reproduce
1. Install NemoClaw v0.0.117 on Ubuntu 22.04 x86_64.
2. Onboard or recreate an OpenClaw CPU sandbox with provider `nvidia-prod` and model `nvidia/nemotron-3-super-120b-a12b`.
3. Run `nemoclaw {sandbox} status` after onboarding reports the sandbox ready.
4. Repeat against more than one freshly-created sandbox lifecycle flow.

## Expected Result
The sandbox status command exits 0 and the Inference row is healthy. The route-reachability and upstream subprobes should agree with a working model invocation through `inference.local`.

## Actual Result
The sandbox status command exits non-zero. The sandbox is in Phase Ready, the inference route is reachable, and in two reproduced flows the upstream provider probe is healthy, but the in-sandbox model invocation through `inference.local` returns HTTP 404 and the Inference row is unhealthy.

## Logs
```text
Sandbox status excerpt from one reproduced flow:
Model:    nvidia/nemotron-3-super-120b-a12b
Provider: nvidia-prod
Inference: unhealthy via inference.local models route
Inference gateway did not serve an inference request: sandbox inference invocation probe returned HTTP 404.
Inference route reachability: reachable
Inference upstream provider probe: healthy
OpenShell: 0.0.106 using docker gateway
Agent:    OpenClaw v2026.7.1

The same HTTP 404 signature reproduced in three independent sandbox lifecycle flows on the Ubuntu 22.04 rerun.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ea68ea444a9f7e27455961ca0412258d47dca489`.  There
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
{"case_id": "NVIDIA_NemoClaw__10879__ea68ea4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
