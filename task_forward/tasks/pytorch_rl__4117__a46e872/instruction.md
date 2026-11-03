# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Dreamerv3 walker doesn't use available GPU, and retains loss tensors

## Describe the bug

The DreamerV3 SOTA walker implementation uses the CPU for all training by default, even when a local GPU is available. The DMC env should run on CPU, but the models, losses, and policy can run on the accelerator.

The trainnig loop also keeps detached loss tensors in memory, 5 scalar tensors per optimisation update. Walker uses ~1M updates, which, if using GPU, makes all these CUDA tensors stay in memory till training ends

## To Reproduce

Install and run on a machine with GPU
```bash
python sota-implementations/dreamer_v3/dreamer_v3.py \
  --config-name=config_dmc_walker
```

Open a second terminal. Monitor the active CUDA processes:

```bash
watch -n 0.5 \
  'nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv'
```

GPU usage stays low, training stays on the CPU

The training loop adds detached tensors to lists after each optimization
update:

```python
loss_hist["kl"].append(model_kl.detach())
loss_hist["reco"].append(m_td["loss_model_reco"].detach())
loss_hist["reward"].append(m_td["loss_model_reward"].detach())
loss_hist["actor"].append(a_td["loss_actor"].detach())
loss_hist["value"].append(v_td["loss_value"].detach())
```

The `detach()` operation removes a tensor from the autograd graph. It does not
move the tensor to the CPU. It does not release the tensor storage.

## Expected behavior

The real DMC env runs on CPU, the models, losses, policy, replay samples run on an available accelerator by default. User can select CPU for training if needed

Only a limited amount of loss data is kept on the GPU. Keep only full CPU loss history is plot is needed

## Screenshots

Not applicable

## System info


```text
Python: 3.11.16
TorchRL: 0.14.0+ga46e872e
PyTorch: 2.15.0.dev20260816+cu130
TensorDict: 0.14.0+g8e4daaa
NumPy: 2.4.6
dm-control: 1.0.44
MuJoCo: 3.11.0
Platform: Linux
GPU: NVIDIA A100 80GB PCIe
```


```python
import sys

import numpy
import torch
import torchrl

print(torchrl.__version__, torch.__version__, numpy.__version__)
print(sys.version, sys.platform)
print(torch.cuda.is_available(), torch.cuda.device_count())
```

## Additional context

Raising a PR to fix this

## Reason and Possible fixes

The config uses env device as the collector and training device. Training script doesnt move the training modules to an auto selected accelerator. Use separate settings for the real env and training

- an `optimization.device` setting. Use `null` to select an available
  accelerator.
- Keep the real collection and evaluation environments on the CPU.
- Set separate `policy_device`, `env_device`, and `storing_device` values for
  the collector.
- Move the models, losses, and sampled replay batches to the optimization
  device.
- Set `auto_cast_to_device=True` for evaluation rollouts.
- Create `DreamerEnv` on the optimization device. Its base constructor calls
  `world_model.to(self.device)` on shared model parameters.
- Store the loss metrics in one tensor for each batch. Move the loss history to
  the CPU only when the code must make a plot.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a46e872e036e9d9485f45f5bef67295ac1f5637f`.  There
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
{"case_id": "pytorch_rl__4117__a46e872",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
