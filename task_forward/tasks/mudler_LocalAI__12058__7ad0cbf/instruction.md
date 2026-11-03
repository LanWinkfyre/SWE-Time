# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
GPU RAM detection with incorrect VRAM value

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
LocalAI v4.9.0 ROCM (docker.io/localai/localai:latest-gpu-hipblas)

**Environment, CPU architecture, OS, and Version:**
AMD (Strix Halo) RYZEN AI MAX+ 395 w/ Radeon 8060S (gfx1151) with 128GB VRAM
Ubuntu 26.04
ROCM 7.14


**Describe the bug**
LocalAI-Web UI is showing on the models page (/app/models): "Your Host: 512 MB GPU RAM"
It seems to me that Local.AI is not determining the VRAM correctly for my setup. 
My LocalAI-Server now is the first application showing 512 MB VRAM (which is my BIOS setting for UMA according to all recommendations and best practises). In grub arguments i adviced the OS to utilize 120 GB GPU VRAM.
I do not want to use a higher BIOS UMA fixed value, as the maximum there is 96GB.
I have installed several AI servers which worked flawless with the 120 GiB VRAM available. 
Loved Locale.AI so far - but unfortunately now I cannot load my models in Local.Ai. 
I did not find a configuration to ensure my VRAM is detected and usable.

I know my gfx1151 is not yet fully supported, but i tried changing in BIOS to 96 GB - it worked.

$ rocm-smi --showmeminfo vram
GPU[0]		: VRAM Total Memory (B): 536870912 (512 MB)     ---------> according to my UMA BIOS Setting
GPU[0]		: VRAM Total Used Memory (B): 507244544 (507 MB)

$ rocm-smi --showmeminfo gtt
GPU[0]		: GTT Total Memory (B): 128849018880 --------> 120 GiB
GPU[0]		: GTT Total Used Memory (B): 442163200 

$ dmesg | egrep "amdgpu .*memory"
[   19.112716] amdgpu 0000:c5:00.0:  512M of VRAM memory ready
[   19.112719] amdgpu 0000:c5:00.0:  122880M of GTT memory ready. ----> 120 GB

$rocminfo (excerpt)

Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    128644892(0x7aaf71c) KB   ------------------> 120 GB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                           

**To Reproduce**
Install Ubuntu, docker compose, portainer, local-ai rocm

**Expected behavior**
I expect Local.Ai to find my available VRAM.

** docker: compose.yaml **

services:
  local-ai:
    image: docker.io/localai/localai:latest-gpu-hipblas
    container_name: local-ai-rocm
    ports:
      - "8080:8080"
    volumes:
      - localai-models:/models
      - localai-backends:/backends
      - localai-configuration:/configuration
      - localai-data:/data
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri
    group_add:
      - "44"   # Video GID
      - "990"  # Render GID
    ipc: host
    security_opt:
      - seccomp=unconfined
    restart: unless-stopped
    environment:
      - HSA_OVERRIDE_GFX_VERSION=11.0.0
      - GGML_AMDGPU_FORCE_VRAM=120GB    # tried this
      - GGML_CUDA_ENABLE_UNIFIED_MEMORY=1   # tried this
      - LOCALAI_VRAM_BUDGET=120GB     # tried this
      - DEBUG=true
      - THREADS=4

volumes:
  localai-models:
  localai-backends:
  localai-configuration:
  localai-data:


**Logs**
DEBUG:
Attaching to local-ai-rocm
local-ai-rocm  | CPU info:
local-ai-rocm  | model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
local-ai-rocm  | flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good amd_lbr_v2 nopl xtopology nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpuid_fault cpb cat_l3 cdp_l3 hw_pstate ssbd mba perfmon_v2 ibrs ibpb stibp ibrs_enhanced vmmcall fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm rdt_a avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local user_shstk avx_vnni avx512_bf16 clzero irperf xsaveerptr rdpru wbnoinvd cppc arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold avic v_vmsave_vmload vgif x2avic v_spec_ctrl vnmi avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid bus_lock_detect movdiri movdir64b overflow_recov succor smca fsrm avx512_vp2intersect flush_l1d amd_lbr_pmc_freeze
local-ai-rocm  | CPU:    AVX    found OK
local-ai-rocm  | CPU:    AVX2   found OK
local-ai-rocm  | CPU:    AVX512 found OK
local-ai-rocm  | Sep 14 20:51:28 DEBUG GPU vendor detected via ghw vendor="amd" caller={caller.file="/build/pkg/xsysinfo/gpu.go"  caller.L=240 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG GPU vendor gpuVendor="amd" caller={caller.file="/build/pkg/system/state.go"  caller.L=87 } 


**local-ai-rocm  | Sep 14 20:51:28 DEBUG VRAM detected via binary tools total_vram=536870912 caller={caller.file="/build/pkg/xsysinfo/gpu.go"  caller.L=149 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG Total available VRAM vram=536870912 caller={caller.file="/build/pkg/system/state.go"  caller.L=89 }**


local-ai-rocm  | Sep 14 20:51:28 INFO  Using forced capability run file capabilityRunFile="/run/localai/capability" capability="amd\n" env="" caller={caller.file="/build/pkg/system/capabilities.go"  caller.L=358 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  VRAM allocation budget set budget="120GB" caller={caller.file="/build/core/cli/run.go"  caller.L=747 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG runtime_settings.json not found, using defaults caller={caller.file="/build/core/application/startup.go"  caller.L=572 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  Starting LocalAI threads=4 modelsPath="//models" caller={caller.file="/build/core/application/startup.go"  caller.L=68 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  LocalAI version version="v4.9.0 (f7ad3f70eb5d8a0ddf80e08557f0d7df28cf032e)" caller={caller.file="/build/core/application/startup.go"  caller.L=69 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  LocalAI Assistant in-memory MCP server initialised tools=39 read_only=false caller={caller.file="/build/core/http/endpoints/mcp/localai_assistant.go"  caller.L=78 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG CPU capabilities capabilities=[3dnowprefetch abm adx aes amd_lbr_pmc_freeze amd_lbr_v2 aperfmperf apic arat avic avx avx2 avx512_bf16 avx512_bitalg avx512_vbmi2 avx512_vnni avx512_vp2intersect avx512_vpopcntdq avx512bw avx512cd avx512dq avx512f avx512ifma avx512vbmi avx512vl avx_vnni bmi1 bmi2 bpext bus_lock_detect cat_l3 cdp_l3 clflush clflushopt clwb clzero cmov cmp_legacy constant_tsc cpb cppc cpuid cpuid_fault cqm cqm_llc cqm_mbm_local cqm_mbm_total cqm_occup_llc cr8_legacy cx16 cx8 de decodeassists erms extapic extd_apicid f16c flush_l1d flushbyasid fma fpu fsgsbase fsrm fxsr fxsr_opt gfni ht hw_pstate ibpb ibrs ibrs_enhanced ibs invpcid irperf lahf_lm lbrv lm mba mca mce misalignsse mmx mmxext monitor movbe movdir64b movdiri msr mtrr mwaitx nonstop_tsc nopl npt nrip_save nx ospke osvw overflow_recov pae pat pausefilter pclmulqdq pdpe1gb perfctr_core perfctr_llc perfctr_nb perfmon_v2 pfthreshold pge pku pni popcnt pse pse36 rapl rdpid rdpru rdrand rdseed rdt_a rdtscp rep_good sep sha_ni skinit smap smca smep ssbd sse sse2 sse4_1 sse4_2 sse4a ssse3 stibp succor svm svm_lock syscall tce topoext tsc tsc_adjust tsc_scale umip user_shstk v_spec_ctrl v_vmsave_vmload vaes vgif vmcb_clean vme vmmcall vnmi vpclmulqdq wbnoinvd wdt x2avic xgetbv1 xsave xsavec xsaveerptr xsaveopt xsaves xtopology] caller={caller.file="/build/core/application/startup.go"  caller.L=77 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG GPU count count=1 caller={caller.file="/build/core/application/startup.go"  caller.L=81 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG GPU gpu="card #1 @0000:c5:00.0 -> driver: 'amdgpu' class: 'Display controller' vendor: 'Advanced Micro Devices, Inc. [AMD/ATI]' product: 'unknown'" caller={caller.file="/build/core/application/startup.go"  caller.L=83 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  stats: using in-memory ring buffer (no-auth single-user mode) caller={caller.file="/build/core/application/startup.go"  caller.L=219 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  stats: fallback user wired local_user_id="af1e0a9f-7f4c-40de-b224-2332b901c947" caller={caller.file="/build/core/application/startup.go"  caller.L=229 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG agent_tasks.json not found, starting with empty tasks caller={caller.file="/build/core/services/agentpool/job_persister_file.go"  caller.L=88 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  Loaded tasks from persister count=0 caller={caller.file="/build/core/services/agentpool/agent_jobs.go"  caller.L=193 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG agent_jobs.json not found, starting with empty jobs caller={caller.file="/build/core/services/agentpool/job_persister_file.go"  caller.L=121 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  Loaded jobs from persister count=0 caller={caller.file="/build/core/services/agentpool/agent_jobs.go"  caller.L=172 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  AgentJobService started retention_days=30 caller={caller.file="/build/core/services/agentpool/agent_jobs.go"  caller.L=1475 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG No system backends found caller={caller.file="/build/core/gallery/backends.go"  caller.L=650 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  Preloading models path="//models" caller={caller.file="/build/core/config/model_config_loader.go"  caller.L=419 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG reading file for dynamic config update filename="/configuration/api_keys.json" caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=65 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG processing api keys runtime update numKeys=0 caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=138 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG no API keys discovered from dynamic config file caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=152 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG total api keys after processing numKeys=0 caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=155 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG reading file for dynamic config update filename="/configuration/external_backends.json" caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=65 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG processing external_backends.json caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=164 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG external backends loaded from external_backends.json caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=181 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG reading file for dynamic config update filename="/configuration/runtime_settings.json" caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=65 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG processing runtime_settings.json caller={caller.file="/build/core/application/config_file_watcher.go"  caller.L=189 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  core/startup process completed! caller={caller.file="/build/core/application/startup.go"  caller.L=531 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG Enabling CSRF middleware (Sec-Fetch-Site mode) caller={caller.file="/build/core/http/app.go"  caller.L=439 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  LocalAI is started and running address=":8080" caller={caller.file="/build/core/cli/run.go"  caller.L=787 } 
local-ai-rocm  | Sep 14 20:51:28 DEBUG HTTP request method="GET" path="/api/operations" status=200 caller={caller.file="/build/core/http/app.go"  caller.L=325 } 
local-ai-rocm  | Sep 14 20:51:28 INFO  Agent pool started (standalone/LocalAGI mode) stateDir="//data" apiURL="http://127.0.0.1:8080" caller={caller.file="/build/core/services/agentpool/agent_pool.go"  caller.L=338 } 
local-ai-rocm  | Sep 14 20:51:29 DEBUG Failed to parse config_file for backend resolution url="github:mudler/LocalAI/gallery/vllm.yaml@master" error=yaml: unmarshal errors:
local-ai-rocm  |   line 5: mapping key "backend" already defined at line 1 caller={caller.file="/build/core/gallery/backend_resolve.go"  caller.L=186 } 
local-ai-rocm  | Sep 14 20:51:29 DEBUG HTTP request method="GET" path="/api/operations" status=200 caller={caller.file="/build/core/http/app.go"  caller.L=325 }
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7ad0cbf259f0c7bf9920fe2438fc3630ecd6c672`.  There
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
{"case_id": "mudler_LocalAI__12058__7ad0cbf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
