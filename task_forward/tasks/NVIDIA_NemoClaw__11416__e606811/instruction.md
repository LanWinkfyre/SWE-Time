# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Inference] managed llama.cpp serving profiles are not offered by profiles list, --profile, or the interactive menu

## Description

Every llama-cpp-backend serving profile is reported as incompatible by nemoclaw profiles
list, is rejected when passed to onboard with --profile, and is absent from the
interactive provider menu. All three discoverable entry points refuse the same profiles
with the message that the backend is not available through Express onboarding yet, while
documentation states the Muse Glimmer managed llama.cpp profile is selectable.

Scope note: the profile is not completely unreachable - it can still be selected by
setting the recipe environment variable directly. The defect is that the three
discoverable, documented entry points do not offer it, so a user following the
documentation cannot reach it.

Impact on test coverage: managed llama.cpp profile selection cannot be exercised at all
through the supported entry points on this build, which blocks verification of the
managed llama.cpp lifecycle and coexistence scenarios.

Platform scope: Reproduced on DGX Spark GB10 aarch64 and on Ubuntu x86_64; the same
message appears on both.
Regression: Unknown - earlier versions not tested for this path.
OpenShell issue: No

## Environment

```text
Device:        DGX Spark GB10
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.2.1, build a5c7197
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.121
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. On a qualified DGX Spark host with NemoClaw installed, list the serving profiles:

     nemoclaw profiles list

2. Try to onboard using a managed llama.cpp Muse Glimmer profile by name:

     nemoclaw onboard --name muse-llamacpp-life \
       --profile llama-cpp.dgx-spark-gb10.single.muse-glimmer-30b --fresh --yes

3. Run interactive onboarding and inspect the inference provider menu for a managed
   llama.cpp Muse Glimmer option:

     NEMOCLAW_EXPERIMENTAL=1 nemoclaw onboard --name muse-check
```

## Expected Result

The managed llama.cpp Muse Glimmer profile that documentation says is selectable can be
selected through at least one discoverable entry point - listed as compatible by profiles
list, accepted by --profile, or offered in the interactive menu.

## Actual Result

Step 1: every llama-cpp-backend catalog entry, including the matching Spark GB10 entry, is
annotated:

  incompatible: Backend install-llama-cpp is not available through Express onboarding yet.

Step 2, verbatim:

  Serving profile 'llama-cpp.dgx-spark-gb10.single.muse-glimmer-30b' is incompatible:
  Backend install-llama-cpp is not available through Express onboarding yet.

  exit code 1

Step 3: no managed llama.cpp Muse Glimmer option appears in the provider menu.

This was observed on two separate runs on v0.0.121 with identical wording.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e6068115cc5e02e0d05abdb46ea4509138847617`.  There
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
{"case_id": "NVIDIA_NemoClaw__11416__e606811",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
