# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
v2.ElasticTransform raises IndexError when BoundingBoxes coordinates touch the image boundary

### 🐛 Describe the bug

#### Bug description

v2.ElasticTransform crashes with an IndexError when applied to BoundingBoxes whose XYXY coordinates equal the canvas dimensions (e.g. x2=W or y2=H). These should be semantically valid coordinates, specifying that the box extends to the image edge, but the internal grid lookup in [elastic_bounding_boxes()](https://github.com/pytorch/vision/blob/main/torchvision/transforms/v2/functional/_geometry.py#L2459-L2469) uses them as array indices without clamping.

In elastic_bounding_boxes(), bbox corners are ceil()-ed, cast to long, and used directly to index into inv_grid of shape (1, H, W, 2):
```python
points = points.ceil_()
index_xy = points.to(dtype=torch.long)
index_x, index_y = index_xy[:, 0], index_xy[:, 1]
transformed_points = inv_grid[0, index_y, index_x, :]  # IndexError here
```

Valid indices are 0..H-1 and 0..W-1, but x2=W / y2=H produce index W / H which are out of bounds.
This is easy to hit in practice: any bounding box that touches the image edge (common after v2.Resize) will trigger the crash.

#### Minimal reproducer
```python
import torch
from torchvision import tv_tensors
from torchvision.transforms import v2

SIZE = 512
image = tv_tensors.Image(torch.randint(0, 255, (3, SIZE, SIZE), dtype=torch.uint8))

# Bbox touching the image edge — valid XYXY coordinates
bbox = tv_tensors.BoundingBoxes(
    torch.tensor([[0, 0, SIZE, SIZE]], dtype=torch.float32),
    format=tv_tensors.BoundingBoxFormat.XYXY,
    canvas_size=(SIZE, SIZE),
)

transform = v2.ElasticTransform(alpha=50.0, sigma=5.0)
transform(image, bbox)  # IndexError
```

Gives the error:
````
  File "/home/ubuntu/spark-2026-stream-1/.venv/lib/python3.12/site-packages/torchvision/transforms/v2/functional/_geometry.py", line 2435, in elastic_bounding_boxes
    transformed_points = inv_grid[0, index_y, index_x, :].add_(1).mul_(0.5 * t_size).sub_(0.5)
                         ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: index 512 is out of bounds for dimension 1 with size 512
````

#### Notes
- Works fine without BoundingBoxes (image + mask only).
- Works fine when bbox coords are strictly inside the image (e.g. [10, 10, 502, 502]), only fails when any corner coordinate equals the canvas dimension.
- A clamp before the grid indexing would fix this:
```python
  index_x = index_x.clamp(0, canvas_size[1] - 1)
  index_y = index_y.clamp(0, canvas_size[0] - 1)
```


### Versions

PyTorch version: 2.10.0+cu128
Is debug build: False
CUDA used to build PyTorch: 12.8
ROCM used to build PyTorch: N/A

OS: Ubuntu 24.04.2 LTS (x86_64)
GCC version: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
CMake version: version 3.28.3
Libc version: glibc-2.39

Python version: 3.12.11 (main, Jul  1 2025, 18:37:24) [Clang 20.1.4 ] (64-bit runtime)
Python platform: Linux-6.14.0-1018-aws-x86_64-with-glibc2.39
Is CUDA available: True
CUDA runtime version: 12.8.93
GPU models and configuration: GPU 0: NVIDIA A10G
Nvidia driver version: 580.105.08

Versions of relevant libraries:
[pip3] torch==2.10.0
[pip3] torchvision==0.25.0
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8a5946ed6bce34bfeb26b964fc8875447d841ae8`.  There
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
{"case_id": "pytorch_vision__9394__8a5946e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
