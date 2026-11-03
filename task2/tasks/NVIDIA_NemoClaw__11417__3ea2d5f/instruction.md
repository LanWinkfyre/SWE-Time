# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Sandbox] rebuild drops serving profile provenance from the sandbox registry

## Description

A sandbox onboarded with an explicit managed vLLM serving profile reports its serving
profile, serving recipe and catalog digest in nemoclaw status. After a successful rebuild
those three lines are gone from status, permanently. Provider, model, phase and inference
health remain correct and the sandbox works, so nothing visibly breaks - the provenance
information is simply no longer recorded and cannot be recovered from the CLI.

The rebuild otherwise preserves the serving configuration: the rebuilt sandbox serves the
same profile and model, runs in resume mode without re-selecting a model, and does not
re-download the model. So the provenance loss is inconsistent with the rest of the
rebuild's behaviour.

Consequence: after any rebuild there is no supported way to confirm from the CLI which
serving profile a sandbox is actually running.

Platform scope: Reproduced on DGX Spark GB10 aarch64 only; other platforms not tested.
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
1. Onboard a sandbox with an explicit managed vLLM serving profile:

     nemoclaw onboard --name muse-vllm-life \
       --profile vllm.dgx-spark-gb10.single.muse-glimmer-30b-nvfp4-w4a4 \
       --fresh --non-interactive --yes --yes-i-accept-third-party-software

2. Record the profile-related lines:

     nemoclaw muse-vllm-life status

3. Rebuild the sandbox and confirm it exits 0:

     nemoclaw muse-vllm-life rebuild --yes

4. Compare status again:

     nemoclaw muse-vllm-life status
```

## Expected Result

A successful rebuild preserves the sandbox's serving configuration, so status keeps
reporting the same serving profile, serving recipe and catalog digest afterwards.

## Actual Result

Step 2, before rebuild, status includes lines of the form:

  Serving profile: vllm.dgx-spark-gb10.single.muse-glimmer-30b-nvfp4-w4a4
  Serving recipe:  {recipe id}
  Catalog digest:  {digest}

Step 3 succeeds:

  Sandbox 'muse-vllm-life' rebuild completed
  Now running: OpenClaw v2026.7.1

  exit code 0

Step 4, after rebuild, those three lines are no longer printed at all. Status is not
reporting an error - the fields are simply absent.

Everything else about the rebuild is correct in the same run: provider and model are still
vllm-local / muse-glimmer before and after, the rebuild ran in resume mode without asking
to select a model, and the 23.7 GiB model was not re-downloaded (about 58 seconds to
re-create versus roughly 7 minutes for the original onboard). An agent request returned
its expected marker both before and after the rebuild.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3ea2d5f9a515d4176e0745214743a48ff4868f4c`.  There
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
{"case_id": "NVIDIA_NemoClaw__11417__3ea2d5f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
