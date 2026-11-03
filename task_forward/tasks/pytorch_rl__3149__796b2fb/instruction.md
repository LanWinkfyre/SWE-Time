# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Add Diffusion Policy modules (Actor + Loss + Example)

## Motivation

- Diffusion-based policies (e.g., Diffusion Policy, Diffusion-QL) have demonstrated strong empirical results in robotics and offline RL.

## Solution

**Solution (Plan & References)**
We will implement Phase-1 by **adapting the core ideas and minimal components** from the *Diffusion Policy* work—*Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*—and its official codebase, aligning them with TorchRL’s API patterns (TensorDict/Modules/Objectives/Transforms).

* **Primary references**

  * Paper & project page: *Diffusion Policy* (RSS 2023 / IJRR), with public project materials, data, and logs. ([[GitHub](https://github.com/real-stanford/diffusion_policy?tab=readme-ov-file)][1])
  * Official code repository: `real-stanford/diffusion_policy` (training configs, scripts, and Colab demos for state/vision tasks). ([[GitHub](https://github.com/real-stanford/diffusion_policy?tab=readme-ov-file)][1])

* **What we will port/adapt**

  1. **Actor (DiffusionActor)**

     * A score-based policy that denoises latent actions conditioned on observations—implemented as `torchrl.modules.DiffusionActor`.
     * Pluggable **score network** (e.g., small MLP for low-dim control; CNN encoder later for pixels), **scheduler** (DDPM-style first), and `num_steps`.
     * Strict **TensorDict** contract: `in_keys=["observation"]` → `out_keys=["action"]`.
  2. **Objective (DiffusionBCLoss)**

     * Supervised denoising/ε-prediction loss and a score-matching variant for imitation learning, following the paper’s training target while fitting TorchRL’s Objective API.
     
-  **Example & Repro Path**

     * `examples/diffusion_bc_pendulum.py` (state-based control) to mirror the repo’s low-dim examples first.
     * Clear instructions to plug in public training data/config patterns analogous to the reference repo’s setup (e.g., single-seed + multi-seed runs). ([[GitHub](https://github.com/real-stanford/diffusion_policy?tab=readme-ov-file)][1])


## Checklist

* [x] I have checked that there is no similar issue in the repo (**required**)
* [x] This request aligns with TorchRL’s [[call for contributions](https://github.com/pytorch/rl/issues/509)](https://github.com/pytorch/rl/issues) (feature proposals & new algorithm implementations).
* [x] I will take ownership of this feature request and open PR(s) to implement **Phase-1 (Actor + Loss + Example)**.
* [ ] The implementation plan references **[[Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://github.com/real-stanford/diffusion_policy?tab=readme-ov-file)](https://github.com/real-stanford/diffusion_policy?tab=readme-ov-file)** (paper + code) and adapts it to TorchRL’s API patterns (Modules/Objectives/Collectors).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `796b2fb1f70d29f22fcc739178a8c8547998696f`.  There
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
{"case_id": "pytorch_rl__3149__796b2fb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
