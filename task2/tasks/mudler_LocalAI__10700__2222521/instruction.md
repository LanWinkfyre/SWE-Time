# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Model `ornith-1.0-9b-mtp` wrongly reported as "Size: 71.2 GB · VRAM: 71.2 GB" (size of the entire HF repository) in "Install Models" gallery

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
v4.6.1, installed using Linux launcher

**Environment, CPU architecture, OS, and Version:**
Linux miki-linux-ai 7.1.3-1-cachyos #1 SMP PREEMPT_DYNAMIC Sat, 04 Jul 2026 20:05:25 +0000 x86_64 GNU/Linux
CPU: Ryzen 9950X3D
RAM: 64 GB
GPU: RTX 5080

**Describe the bug**
In the "Install Models" gallery, the model `ornith-1.0-9b-mtp` is wrongly reported as "Size: 71.2 GB · VRAM: 71.2 GB" and "May not fit", which is to be expected for my RTX 5080 GPU, as the reported size is the size of the entire Hugging Face repository, not just the needed GGUF file.

**To Reproduce**
1. In the LocalAI Web UI, switch to "Import Models" tab.
2. Search for "ornith".

**Expected behavior**
The model's actual size as per the model file on Hugging Face should be reported, not the size of the entire repository, which contains several model variants with different quantizations.

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
The model definition in `gallery/index.yaml` correctly lists the model file URI as: https://huggingface.co/protoLabsAI/Ornith-1.0-9B-MTP-GGUF/resolve/main/ornith-9b-mtp-kl-Q4_K_M.gguf
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `22225217e036c624038120fd085084367e76a9ba`.  There
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
{"case_id": "mudler_LocalAI__10700__2222521",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
