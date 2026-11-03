# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
`v2.ElasticTransform` applies incorrect vertical/horizontal normalization on displacement vectors

### 🐛 Describe the bug

### Bug Description

I believe there is a logic error in `torchvision.transforms.v2.ElasticTransform`. The implementation swaps the spatial dimensions when normalizing the displacement vectors, leading to incorrect anisotropic deformation on non-square inputs.

**The Logic:**
The `make_params` method generates random displacement fields `dx` (horizontal) and `dy` (vertical). To use these with `grid_sample`, they must be normalized to the $[-1, 1]$ coordinate space.

  * Horizontal displacement (`dx`) should be normalized by the **Width**.
  * Vertical displacement (`dy`) should be normalized by the **Height**.

**The Code:**
In `torchvision/transforms/v2/_geometry.py`, the code does the reverse:

```python
# size is (Height, Width) because it comes from query_size(flat_inputs)
size = list(query_size(flat_inputs)) 

# ... (dx generation) ...

# BUG: dx (Horizontal shift) is divided by size[0] (Height)
dx = dx * self.alpha[0] / size[0]

# ... (dy generation) ...

# BUG: dy (Vertical shift) is divided by size[1] (Width)
dy = dy * self.alpha[1] / size[1]
```

### Consequence

If the input image is non-square (e.g., $W \gg H$), the horizontal displacement is divided by a small number ($H$), causing extreme distortion. The vertical displacement is divided by a large number ($W$), causing almost no distortion.

### Reproduction Code

Here is a script that creates a $100 \times 800$ grid image.

1.  **Standard:** Applies the current `v2.ElasticTransform`.
2.  **Patched:** Applies a subclass with corrected divisors.

<!-- end list -->

```python
import torch
import matplotlib.pyplot as plt
from torchvision.transforms import v2
from torchvision.transforms.v2 import functional as F
from torchvision.transforms.v2._utils import query_size

# 1. Setup helper to create a Grid Image
def create_grid_image(h, w, spacing=20):
    img = torch.ones((1, h, w))
    img[:, :, ::spacing] = 0 # Vertical lines
    img[:, ::spacing, :] = 0 # Horizontal lines
    return img

# 2. Define the "Patched" Transform (Correct Logic)
class PatchedElasticTransform(v2.ElasticTransform):
    def make_params(self, flat_inputs):
        size = list(query_size(flat_inputs)) # Returns (H, W)
        
        dx = torch.rand([1, 1] + size) * 2 - 1
        if self.sigma[0] > 0.0:
            kx = int(8 * self.sigma[0] + 1)
            if kx % 2 == 0: kx += 1
            dx = self._call_kernel(F.gaussian_blur, dx, [kx, kx], list(self.sigma))
            
        # FIX: Normalize x-displacement by Width (size[1])
        dx = dx * self.alpha[0] / size[1] 

        dy = torch.rand([1, 1] + size) * 2 - 1
        if self.sigma[1] > 0.0:
            ky = int(8 * self.sigma[1] + 1)
            if ky % 2 == 0: ky += 1
            dy = self._call_kernel(F.gaussian_blur, dy, [ky, ky], list(self.sigma))
        
        # FIX: Normalize y-displacement by Height (size[0])
        dy = dy * self.alpha[1] / size[0]

        displacement = torch.concat([dx, dy], 1).permute([0, 2, 3, 1])
        return dict(displacement=displacement)

# 3. Visualization
torch.manual_seed(42)
H, W = 100, 800
img = create_grid_image(H, W, spacing=25)
alpha = 100.0 
sigma = 10.0

# Standard (Buggy)
t_standard = v2.ElasticTransform(alpha=alpha, sigma=sigma)
torch.manual_seed(10)
out_standard = t_standard(img)

# Patched (Fixed)
t_patched = PatchedElasticTransform(alpha=alpha, sigma=sigma)
torch.manual_seed(10)
out_patched = t_patched(img)

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(10, 8))
axs[0].imshow(img.permute(1, 2, 0), cmap='gray'); axs[0].set_title(f"Original (H={H}, W={W})")
axs[1].imshow(out_standard.permute(1, 2, 0), cmap='gray'); axs[1].set_title("Standard v2 (Current Implementation)")
axs[2].imshow(out_patched.permute(1, 2, 0), cmap='gray'); axs[2].set_title("Patched Implementation")
plt.tight_layout()
plt.show()
```

### Results

<img width="1000" height="800" alt="Image" src="https://github.com/user-attachments/assets/fdc06461-7356-4b37-95d8-f26c579b2b89" />

**Observation:**
In the "Standard v2" result, the vertical lines are extremely wavy (huge horizontal noise) because they are normalized by the small height. The horizontal lines are straight (tiny vertical noise) because they are normalized by the large width. The "Patched" result shows uniform distortion.

### Proposed Fix

In `torchvision/transforms/v2/_geometry.py`, the divisors should be swapped to match the axis they represent.

```python
    def make_params(self, flat_inputs: list[Any]) -> dict[str, Any]:
        size = list(query_size(flat_inputs))

        # ... (dx calculation) ...
        
        # PROPOSED CHANGE: Normalize dx by Width (size[1])
        dx = dx * self.alpha[0] / size[1]

        # ... (dy calculation) ...

        # PROPOSED CHANGE: Normalize dy by Height (size[0])
        dy = dy * self.alpha[1] / size[0]
        
        displacement = torch.concat([dx, dy], 1).permute([0, 2, 3, 1])
        return dict(displacement=displacement)
```

**Note on alpha/sigma sequence:**
This fix assumes `alpha` and `sigma` tuples are provided in `(x, y)` order. The current implementation implicitly treats `alpha[0]` as the multiplier for `dx`. Since `size` comes from `query_size` (returning `H, W`), `size[0]` is `H` and `size[1]` is `W`. The mismatch likely arose from conflating `(H, W)` tensor dimensions with `(x, y)` coordinate systems.



### Versions

Collecting environment information...
PyTorch version: 2.9.1+cu128
Is debug build: False
CUDA used to build PyTorch: 12.8
ROCM used to build PyTorch: N/A

OS: Debian GNU/Linux 12 (bookworm) (x86_64)
GCC version: (Debian 12.2.0-14+deb12u1) 12.2.0
Clang version: 14.0.6
CMake version: version 3.25.1
Libc version: glibc-2.36

Python version: 3.12.12 | packaged by conda-forge | (main, Oct 22 2025, 23:25:55) [GCC 14.3.0] (64-bit runtime)
Python platform: Linux-6.1.0-41-amd64-x86_64-with-glibc2.36
Is CUDA available: False
CUDA runtime version: No CUDA
CUDA_MODULE_LOADING set to: N/A
GPU models and configuration: No CUDA
Nvidia driver version: No CUDA
cuDNN version: No CUDA
Is XPU available: False
HIP runtime version: N/A
MIOpen runtime version: N/A
Is XNNPACK available: True

CPU:
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           48 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  24
On-line CPU(s) list:                     0-23
Vendor ID:                               AuthenticAMD
Model name:                              AMD Ryzen 9 9900X 12-Core Processor
CPU family:                              26
Model:                                   68
Thread(s) per core:                      2
Core(s) per socket:                      12
Socket(s):                               1
Stepping:                                0
Frequency boost:                         enabled
CPU(s) scaling MHz:                      43%
CPU max MHz:                             8696.8750
CPU min MHz:                             3000.0000
BogoMIPS:                                8782.92
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good amd_lbr_v2 nopl nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba perfmon_v2 ibrs ibpb stibp ibrs_enhanced vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local avx_vnni avx512_bf16 clzero irperf xsaveerptr rdpru wbnoinvd cppc arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload vgif v_spec_ctrl avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid bus_lock_detect movdiri movdir64b overflow_recov succor smca fsrm avx512_vp2intersect flush_l1d amd_lbr_pmc_freeze
Virtualization:                          AMD-V
L1d cache:                               576 KiB (12 instances)
L1i cache:                               384 KiB (12 instances)
L2 cache:                                12 MiB (12 instances)
L3 cache:                                64 MiB (2 instances)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-23
Vulnerability Gather data sampling:      Not affected
Vulnerability Indirect target selection: Not affected
Vulnerability Itlb multihit:             Not affected
Vulnerability L1tf:                      Not affected
Vulnerability Mds:                       Not affected
Vulnerability Meltdown:                  Not affected
Vulnerability Mmio stale data:           Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Not affected
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; Enhanced / Automatic IBRS; IBPB conditional; STIBP always-on; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                     Not affected
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Not affected
Vulnerability Vmscape:                   Not affected

Versions of relevant libraries:
[pip3] numpy==2.3.5
[pip3] nvidia-cublas-cu12==12.8.4.1
[pip3] nvidia-cuda-cupti-cu12==12.8.90
[pip3] nvidia-cuda-nvrtc-cu12==12.8.93
[pip3] nvidia-cuda-runtime-cu12==12.8.90
[pip3] nvidia-cudnn-cu12==9.10.2.21
[pip3] nvidia-cufft-cu12==11.3.3.83
[pip3] nvidia-curand-cu12==10.3.9.90
[pip3] nvidia-cusolver-cu12==11.7.3.90
[pip3] nvidia-cusparse-cu12==12.5.8.93
[pip3] nvidia-cusparselt-cu12==0.7.1
[pip3] nvidia-nccl-cu12==2.27.5
[pip3] nvidia-nvjitlink-cu12==12.8.93
[pip3] nvidia-nvtx-cu12==12.8.90
[pip3] torch==2.9.1
[pip3] torchvision==0.24.1
[pip3] triton==3.5.1
[conda] numpy                     2.3.5                    pypi_0    pypi
[conda] nvidia-cublas-cu12        12.8.4.1                 pypi_0    pypi
[conda] nvidia-cuda-cupti-cu12    12.8.90                  pypi_0    pypi
[conda] nvidia-cuda-nvrtc-cu12    12.8.93                  pypi_0    pypi
[conda] nvidia-cuda-runtime-cu12  12.8.90                  pypi_0    pypi
[conda] nvidia-cudnn-cu12         9.10.2.21                pypi_0    pypi
[conda] nvidia-cufft-cu12         11.3.3.83                pypi_0    pypi
[conda] nvidia-curand-cu12        10.3.9.90                pypi_0    pypi
[conda] nvidia-cusolver-cu12      11.7.3.90                pypi_0    pypi
[conda] nvidia-cusparse-cu12      12.5.8.93                pypi_0    pypi
[conda] nvidia-cusparselt-cu12    0.7.1                    pypi_0    pypi
[conda] nvidia-nccl-cu12          2.27.5                   pypi_0    pypi
[conda] nvidia-nvjitlink-cu12     12.8.93                  pypi_0    pypi
[conda] nvidia-nvtx-cu12          12.8.90                  pypi_0    pypi
[conda] torch                     2.9.1                    pypi_0    pypi
[conda] torchvision               0.24.1                   pypi_0    pypi
[conda] triton                    3.5.1                    pypi_0    pypi
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `894601fafb9da035b9a1caf249e93974f7e49651`.  There
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
{"case_id": "pytorch_vision__9299__894601f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
