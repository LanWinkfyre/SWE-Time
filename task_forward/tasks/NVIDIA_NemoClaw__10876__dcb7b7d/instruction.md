# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
vLLM managed install fails: served model name does not match its own shared gateway route for nemotron-3-nano-4b

> [!WARNING]
> **Regression** — a closely related instance of this failure pattern (#10648, Nemotron 3 Ultra 550B on DGX Station) was fixed and closed one day before this was reproduced with a different catalog model (Nemotron 3 Nano 4B) on generic Ubuntu Linux.

## Description

A fresh managed vLLM install via `NEMOCLAW_PROVIDER=install-vllm NEMOCLAW_VLLM_MODEL={catalog-short-alias}` fails onboarding at the final step because the vLLM server's self-reported model identifier does not match the "shared gateway route" name the same onboarding flow itself registered, even on a completely clean install with no pre-existing vLLM server or user customization involved. This is the installer's own internally-started server failing against its own internally-registered route name.

Platform scope: Reproduced on Ubuntu 26.04 only; other platforms not tested.
Regression: Yes — #10648 (a closely related instance of the same failure pattern, for the Nemotron 3 Ultra 550B catalog model on DGX Station) was fixed and closed one day before this was reproduced with a different catalog model (Nemotron 3 Nano 4B) on generic Ubuntu Linux, suggesting the fix for #10648 was scoped to that specific model rather than the underlying alias-vs-reported-identifier reconciliation logic. #7023 documents an earlier, also-fixed instance of the same general pattern for a user's own pre-existing custom-named server.
OpenShell issue: No

## Environment

```text
Device:        Linux GPU test server
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.7.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.118
OpenClaw:      N/A (onboard never completes in this repro)
```

## Steps to Reproduce

1. On a clean Linux host with an NVIDIA GPU, Docker, and `NEMOCLAW_EXPERIMENTAL=1`, run:
   ```bash
   NEMOCLAW_EXPERIMENTAL=1 NEMOCLAW_PROVIDER=install-vllm NEMOCLAW_VLLM_MODEL=nemotron-3-nano-4b nemoclaw onboard --name {sandbox} --non-interactive --yes-i-accept-third-party-software
   ```
2. Wait for the vLLM image pull, model download, and container startup to complete (observed ~2 minutes for this smaller model).
3. Observe onboarding fail at the final step with the model-mismatch error below.
4. If retried after removing the vLLM container entirely (`docker stop/rm nemoclaw-vllm`) and re-running the exact same command, the identical mismatch reproduces again from a fully fresh container.

## Expected Result

Per the documented behavior for `NEMOCLAW_VLLM_MODEL` ("Slugs are case-insensitive, and NemoClaw also accepts the full Hugging Face model ID or a registered served model name" — with `nemotron-3-nano-4b` listed as a supported catalog slug example), a stock managed install using this catalog alias should complete onboarding successfully without any manual naming intervention.

## Actual Result

Onboarding fails with:

```text
  Detected vLLM model 'nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8' does not match the shared gateway route 'nemotron-3-nano-4b'.
  To install 'nemotron-3-nano-4b', stop the existing vLLM server on localhost:8000, then rerun the original install/onboard command.
  To keep 'nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8' instead, start detailed setup:
    unset NEMOCLAW_PROVIDER NEMOCLAW_MODEL NEMOCLAW_VLLM_MODEL
    nemoclaw onboard --fresh
  Then select Local vLLM when prompted.

  Onboarding did not finish. Resume from the step that failed with:
    nemoclaw onboard --resume --name {sandbox}
  Completed steps are skipped; pass --fresh instead to start over.
```

The tool's own suggested remediation ("stop the existing vLLM server, then rerun") does not resolve the problem: stopping and removing the vLLM container and rerunning the identical command reproduces the exact same mismatch from a completely fresh container, since the installer's own alias resolution ("nemotron-3-nano-4b" → "nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8") is what starts the server that then fails to match the installer's own separately-registered route name.

## Logs

```text
  ==> Pulling vLLM image: nvcr.io/nvidia/vllm@sha256:[digest omitted]
  ==> Pre-downloading model with hf: nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8
  ==> Model download complete
  ==> Starting vLLM container (nemoclaw-vllm)
  ==> Launching vLLM
  ⏳ Still working on vLLM install… (60s elapsed)
  ==> vLLM is serving on :8000
  ✓ vLLM ready on localhost:8000
  ✓ Using existing vLLM on localhost:8000
  Detected vLLM model 'nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8' does not match the shared gateway route 'nemotron-3-nano-4b'.
  [remediation text as above]
  Onboarding did not complete successfully.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `dcb7b7d2fe89da539df21977ad40d2aa8328e32b`.  There
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
{"case_id": "NVIDIA_NemoClaw__10876__dcb7b7d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
