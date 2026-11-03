# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Intel Arc Pro B70 VRAM not parsed

**LocalAI version:**
quay.io/go-skynet/local-ai:v4.1.3-gpu-vulkan@sha256:ab337d593517231464cd50fe81fa4f84ee9bda5be0856e2591cdfd5f020a70bf

**Environment, CPU architecture, OS, and Version:**
Linux 7997ab623f44 6.19.10+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.19.10-1~bpo13+1 (2026-04-02) x86_64 x86_64 x86_64 GNU/Linux
AMD Ryzen 7 3700X
Intel Arc Pro B70

**Describe the bug**
The VRAM for my Intel Arc Pro B70 is not detected. Inference works correctly.

**To Reproduce**
Start the container, see only device RAM and no VRAM.

**Expected behavior**
Correctly show used VRAM.

**Logs**
```
Apr 09 08:34:46 DEBUG GPU vendor detected via ghw vendor="intel" caller={caller.file="/build/pkg/xsysinfo/gpu.go"  caller.L=159 }
Apr 09 08:34:46 DEBUG GPU vendor gpuVendor="intel" caller={caller.file="/build/pkg/system/state.go"  caller.L=77 }
Apr 09 08:34:46 DEBUG failed to parse vulkaninfo output error=unexpected end of JSON input caller={caller.file="/build/pkg/xsysinfo/gpu.go"  caller.L=795 }
Apr 09 08:34:46 DEBUG Total available VRAM vram=0 caller={caller.file="/build/pkg/system/state.go"  caller.L=79 }
Apr 09 08:34:46 INFO  Using forced capability run file capabilityRunFile="/run/localai/capability" capability="vulkan\n" env="" caller={caller.file="/build/pkg/system/capabilities.go"  caller.L=98 }
Apr 09 08:34:46 INFO  Starting LocalAI threads=8 modelsPath="//models" caller={caller.file="/build/core/application/startup.go"  caller.L=38 }
Apr 09 08:34:46 INFO  LocalAI version version="v4.1.3 (fdc9f7bf350b05942323f5f4b264480c7b67b51c)" caller={caller.file="/build/core/application/startup.go"  caller.L=39 }
Apr 09 08:34:46 DEBUG CPU capabilities capabilities=[3dnowprefetch abm adx aes aperfmperf apic arat avic avx avx2 bmi1 bmi2 bpext cat_l3 cdp_l3 clflush clflushopt clwb clzero cmov cmp_legacy constant_tsc cpb cpuid cqm cqm_llc cqm_mbm_local cqm_mbm_total cqm_occup_llc cr8_legacy cx16 cx8 de decodeassists extapic extd_apicid f16c flushbyasid fma fpu fsgsbase fxsr fxsr_opt ht hw_pstate ibpb ibs irperf lahf_lm lbrv lm mba mca mce misalignsse mmx mmxext monitor movbe msr mtrr mwaitx nonstop_tsc nopl npt nrip_save nx osvw overflow_recov pae pat pausefilter pclmulqdq pdpe1gb perfctr_core perfctr_llc perfctr_nb pfthreshold pge pni popcnt pse pse36 rapl rdpid rdpru rdrand rdseed rdt_a rdtscp rep_good sep sev sev_es sha_ni skinit smap smca smep ssbd sse sse2 sse4_1 sse4_2 sse4a ssse3 stibp succor svm svm_lock syscall tce topoext tsc tsc_scale umip v_spec_ctrl v_vmsave_vmload vgif vmcb_clean vme vmmcall wbnoinvd wdt x2apic xgetbv1 xsave xsavec xsaveerptr xsaveopt xtopology] caller={caller.file="/build/core/application/startup.go"  caller.L=47 }
Apr 09 08:34:46 DEBUG GPU count count=1 caller={caller.file="/build/core/application/startup.go"  caller.L=52 }
Apr 09 08:34:46 DEBUG GPU gpu="card #0 @0000:0f:00.0 -> driver: 'xe' class: 'Display controller' vendor: 'Intel Corporation' product: 'unknown'" caller={caller.file="/build/core/application/startup.go"  caller.L=54 }
```

**Additional context**
vulkaninfo inside container shows the correct VRAM (although usage is 0). The VRAM is currently loaded with ~24GiB.
```
VkPhysicalDeviceMemoryProperties:
=================================
memoryHeaps: count = 2
	memoryHeaps[0]:
		size   = 34242297856 (0x7f9000000) (31.89 GiB)
		budget = 7537164288 (0x1c1400000) (7.02 GiB)
		usage  = 0 (0x00000000) (0.00 B)
		flags: count = 1
			MEMORY_HEAP_DEVICE_LOCAL_BIT
	memoryHeaps[1]:
		size   = 101233557504 (0x1791fd8000) (94.28 GiB)
		budget = 58268319744 (0xd91100000) (54.27 GiB)
		usage  = 0 (0x00000000) (0.00 B)
		flags:
			None
memoryTypes: count = 7
	memoryTypes[0]:
		heapIndex     = 0
		propertyFlags = 0x0001: count = 1
			MEMORY_PROPERTY_DEVICE_LOCAL_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				color images
				FORMAT_D16_UNORM
				FORMAT_X8_D24_UNORM_PACK32
				FORMAT_D32_SFLOAT
				FORMAT_S8_UINT
				FORMAT_D24_UNORM_S8_UINT
				FORMAT_D32_SFLOAT_S8_UINT
			IMAGE_TILING_LINEAR:
				color images
	memoryTypes[1]:
		heapIndex     = 0
		propertyFlags = 0x0001: count = 1
			MEMORY_PROPERTY_DEVICE_LOCAL_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				color images
				FORMAT_D16_UNORM
				FORMAT_X8_D24_UNORM_PACK32
				FORMAT_D32_SFLOAT
				FORMAT_S8_UINT
				FORMAT_D24_UNORM_S8_UINT
				FORMAT_D32_SFLOAT_S8_UINT
			IMAGE_TILING_LINEAR:
				color images
	memoryTypes[2]:
		heapIndex     = 1
		propertyFlags = 0x000e: count = 3
			MEMORY_PROPERTY_HOST_VISIBLE_BIT
			MEMORY_PROPERTY_HOST_COHERENT_BIT
			MEMORY_PROPERTY_HOST_CACHED_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				color images
				FORMAT_D16_UNORM
				FORMAT_X8_D24_UNORM_PACK32
				FORMAT_D32_SFLOAT
				FORMAT_S8_UINT
				FORMAT_D24_UNORM_S8_UINT
				FORMAT_D32_SFLOAT_S8_UINT
			IMAGE_TILING_LINEAR:
				color images
	memoryTypes[3]:
		heapIndex     = 0
		propertyFlags = 0x0007: count = 3
			MEMORY_PROPERTY_DEVICE_LOCAL_BIT
			MEMORY_PROPERTY_HOST_VISIBLE_BIT
			MEMORY_PROPERTY_HOST_COHERENT_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				color images
				FORMAT_D16_UNORM
				FORMAT_X8_D24_UNORM_PACK32
				FORMAT_D32_SFLOAT
				FORMAT_S8_UINT
				FORMAT_D24_UNORM_S8_UINT
				FORMAT_D32_SFLOAT_S8_UINT
			IMAGE_TILING_LINEAR:
				color images
	memoryTypes[4]:
		heapIndex     = 0
		propertyFlags = 0x0001: count = 1
			MEMORY_PROPERTY_DEVICE_LOCAL_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				None
			IMAGE_TILING_LINEAR:
				None
	memoryTypes[5]:
		heapIndex     = 1
		propertyFlags = 0x000e: count = 3
			MEMORY_PROPERTY_HOST_VISIBLE_BIT
			MEMORY_PROPERTY_HOST_COHERENT_BIT
			MEMORY_PROPERTY_HOST_CACHED_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				None
			IMAGE_TILING_LINEAR:
				None
	memoryTypes[6]:
		heapIndex     = 0
		propertyFlags = 0x0007: count = 3
			MEMORY_PROPERTY_DEVICE_LOCAL_BIT
			MEMORY_PROPERTY_HOST_VISIBLE_BIT
			MEMORY_PROPERTY_HOST_COHERENT_BIT
		usable for:
			IMAGE_TILING_OPTIMAL:
				None
			IMAGE_TILING_LINEAR:
				None
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b88ddce0f337d2901fe99278bd9e16d24b3de224`.  There
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
{"case_id": "mudler_LocalAI__9289__b88ddce",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
