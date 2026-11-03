# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
AttributeError: 'numpy.float64' object has no attribute 'numerator'

### 🐛 Describe the bug

When use write_video and pass a float fps value, this error occurs.

```python
import torch
from torchvision.io import write_video

write_video("test.mp4", (torch.randn(16, 224, 224, 3) * 255).to(torch.uint8), fps=5.0)
```

### Versions

OS: macOS 15.3.1 (arm64)
GCC version: Could not collect
Clang version: 16.0.0 (clang-1600.0.26.6)
CMake version: version 3.31.6
Libc version: N/A

Python version: 3.10.14 (main, Jul 31 2024, 19:44:58) [Clang 15.0.0 (clang-1500.3.9.4)] (64-bit runtime)
Python platform: macOS-15.3.1-arm64-arm-64bit
Is CUDA available: False
CUDA runtime version: No CUDA
CUDA_MODULE_LOADING set to: N/A
GPU models and configuration: No CUDA
Nvidia driver version: No CUDA
cuDNN version: No CUDA
HIP runtime version: N/A
MIOpen runtime version: N/A
Is XNNPACK available: True

CPU:
Apple M1 Pro

Versions of relevant libraries:
[pip3] mypy==1.15.0
[pip3] mypy-extensions==1.0.0
[pip3] numpy==1.26.4
[pip3] torch==2.4.1
[conda] No relevant packages
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4cbf9f333835f48da4d467eb9ad92a2fdfec2caf`.  There
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
{"case_id": "pytorch_vision__8990__4cbf9f3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
