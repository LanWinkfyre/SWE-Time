# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
CPU offload performance regression?

**LocalAI version:**
All versions after #10497
In my case LocalAI v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588) localai/localai:latest-gpu-vulkan

**Environment, CPU architecture, OS, and Version:**
In my case I am using an  Intel(R) Xeon(R) CPU E5-2650 on Ubuntu 24.04 LTS, but it does not matter. 

**Describe the bug**
1. GPU backend packages only llama-cpp-fallback.
2. fallback is explicitly compiled with AVX/AVX2/FMA/F16C/BMI2 OFF.
3. system_info therefore reports only SSE3/SSSE3.
4. objdump proves Q3_K kernel:
   ggml_vec_dot_q3_K_q8_K -> ggml_vec_dot_q3_K_q8_K_generic
5. Before #10497, Vulkan packages shipped llama-cpp-avx2 and selected it automatically.
6. #10497 removed optimized CPU variants solely for GPU-build-time reasons.

In my understanding this leads to lower performance when offloading model layers or experts of MoE models to the CPU. Or am I wrong?

**To Reproduce**
Use a gpu backend like llama-vulkan and offload some layers or experts to the CPU. 

**Expected behavior**
All useful features of the CPU like avx2 should be used.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fb54d0faabb070624e2ed1c3df3ccbd195b1b7d2`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__11254__fb54d0f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
