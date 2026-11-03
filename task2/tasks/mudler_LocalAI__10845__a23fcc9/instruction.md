# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
threads parameters from runtime_settings is ignored

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
Version: v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588)
docker image sha256:e0dcd1e3f1f4ea95a7e6118dbe8c8733fba7567a258fbd28c995d62e0701b020


**Environment, CPU architecture, OS, and Version:**
VM without GPU only cpu

**Describe the bug**
Setting threads in ui, which it is also saved in settings_runtime.json is ignored when starting llm model. Also is incorrectly displayed in UI. 
\# docker exec -it localai-api-1 grep -i threads /configuration/runtime_settings.json
  "threads": 5,

but UI displays Default Threads 16 (this is number of cpu in vm). Also models are started with Threads:16 and it can't be overwrite by setting threads: in yaml definition for llm.
The only way I can limit threads is by using env LOCALAI_THREADS

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->

**Logs**
```text
api-1  | Jul 15 13:43:19 INFO  Starting LocalAI threads=16 modelsPath="//models" caller={caller.file="/build/core/application/startup.go"  caller.L=48 }
api-1  | {%- endif %} {{llama-cpp/models/Qwen_Qwen3.5-2B-Q4_K_M.gguf}  false 0 0x307c2371f708 0x307c2371f710 0x307c2371f718 0x307c2371f700 0x307c2371f7d8 <nil> false 512 false 1 0 0 0 1.5 0x307c2371f7d0 0x307c2371f7c8 0x307c2371f7e0 {false} <nil> map[]  0 0 0 0  } qwen_qwen3.5-2b  0x307c2371f5f8 0x307c2371f600 0x307c2371f7e8 map[] 0x307c2371f78b llama-cpp {     true <nil>  } [FLAG_EMBEDDINGS FLAG_TOKENIZE FLAG_VISION FLAG_COMPLETION FLAG_CHAT] 0x307c23b22d88 [] [] {     0 0  {<nil> <nil> <nil> <nil>} <nil> <nil> <nil> <nil> {  <nil>} false} [] [] []    map[]  {false {false false false false true  false   []}   [] [] []   [] [] []    <nil> false false <nil>} {<nil> 0x307c2371f610 <nil> [] []}  map[] map[] map[] {   0 0  0x307c2371f78a false 0x307c2371f7c0 0x307c2371f7b8 0x307c2371f7b0 0x307c23b22a98 0x307c2371f78a 0x307c2371f78b 0x307c2371f78b 0x307c2371f78b  [] [] [] [] [] 0x307c2371f5e8 false   [] [] 0 false  0   0 false false 0 0 0 false  {0 0 0} map[]  0x307c22cb1c00 false q8_0 q8_0   0 0 0 0 0} {false    false 0   } 0 {0 0} {  <nil>} false []   <nil> <nil> [] [use_jinja:true parallel:2 cache_ram:4096 kv_unified:true cache_idle_slots:true n_threads_batch:3 threads:2 n_threads:1 cache_reuse:256 spec_type:draft-mtp spec_n_max:6 spec_p_min:0.75] [] { } {0 0 false false false false false 0 0 false} {<nil> []} {0  map[] [] []} { [] []   0 0   <nil>} { passthrough     0} {[]} {0 0}} caller={caller.file="/build/core/application/startup.go"  caller.L=435 }




api-1  | {%- endif %} {{llama-cpp/models/Qwen_Qwen3.5-2B-Q4_K_M.gguf}  false 0 0x307c2371f708 0x307c2371f710 0x307c2371f718 0x307c233cd348 0x307c233cd340 <nil> false 512 false 1 0 0 0 1.5 0x307c2371f7d0 0x307c2371f7c8 0x307c2371f7e0 {false} <nil> map[]  0 0 0 0  } qwen_qwen3.5-2b  0x307c2371f5f8 0x307c2371f600 0x307c233cd434 map[] 0x307c2371f78b llama-cpp {     true <nil>  } [FLAG_CHAT FLAG_EMBEDDINGS FLAG_TOKENIZE FLAG_COMPLETION FLAG_VISION] 0x307c2384aa08 [] [] {     0 0  {<nil> <nil> <nil> <nil>} <nil> <nil> <nil> <nil> {  <nil>} false} [] [] []    map[]  {false {false false false false true  false   []}   [] [] []   [] [] []    <nil> false false <nil>} {<nil> 0x307c2371f610 <nil> [] []}  map[] map[] map[] {   0 0  0x307c2371f78a false 0x307c2371f7c0 0x307c2371f7b8 0x307c2371f7b0 0x307c23b22a98 0x307c2371f78a 0x307c2371f78b 0x307c2371f78b 0x307c2371f78b  [] [] [] [] [] 0x307c2371f5e8 false   [] [] 0 false  0   0 false false 0 0 0 false  {0 0 0} map[]  0x307c22cb1c00 false q8_0 q8_0   0 0 0 0 0} {false    false 0   } 0 {0 0} {  <nil>} false []   <nil> <nil> [] [use_jinja:true parallel:2 cache_ram:4096 kv_unified:true cache_idle_slots:true n_threads_batch:3 threads:2 n_threads:1 cache_reuse:256 spec_type:draft-mtp spec_n_max:6 spec_p_min:0.75] [] { } {0 0 false false false false false 0 0 false} {<nil> []} {0  map[] [] []} { [] []   0 0   <nil>} { passthrough     0} {[]} {0 0}} caller={caller.file="/build/core/http/endpoints/openai/chat.go"  caller.L=150 }
api-1  | {%- endif %} {{llama-cpp/models/Qwen_Qwen3.5-2B-Q4_K_M.gguf}  false 0 0x307c2371f708 0x307c2371f710 0x307c2371f718 0x307c233cd348 0x307c233cd340 <nil> false 512 false 1 0 0 0 1.5 0x307c2371f7d0 0x307c2371f7c8 0x307c2371f7e0 {false} <nil> map[]  0 0 0 0  } qwen_qwen3.5-2b  0x307c2371f5f8 0x307c2371f600 0x307c233cd434 map[] 0x307c2371f78b llama-cpp {     true <nil>  } [FLAG_CHAT FLAG_EMBEDDINGS FLAG_TOKENIZE FLAG_COMPLETION FLAG_VISION] 0x307c2384aa08 [] [] {     0 0  {<nil> <nil> <nil> <nil>} <nil> <nil> <nil> <nil> {  <nil>} false} [] [] []    map[]  {false {false false false false true  false   []}   [] [] []   [] [] []    <nil> false false <nil>} {<nil> 0x307c2371f610 <nil> [] []}  map[] map[] map[] {   0 0  0x307c2371f78a false 0x307c2371f7c0 0x307c2371f7b8 0x307c2371f7b0 0x307c23b22a98 0x307c2371f78a 0x307c2371f78b 0x307c2371f78b 0x307c2371f78b  [] [] [] [] [] 0x307c2371f5e8 false   [] [] 0 false  0   0 false false 0 0 0 false  {0 0 0} map[]  0x307c22cb1c00 false q8_0 q8_0   0 0 0 0 0} {false    false 0   } 0 {0 0} {  <nil>} false []   <nil> <nil> [] [use_jinja:true parallel:2 cache_ram:4096 kv_unified:true cache_idle_slots:true n_threads_batch:3 threads:2 n_threads:1 cache_reuse:256 spec_type:draft-mtp spec_n_max:6 spec_p_min:0.75] [] { } {0 0 false false false false false 0 0 false} {<nil> []} {0  map[] [] []} { [] []   0 0   <nil>} { passthrough     0} {[]} {0 0}} caller={caller.file="/build/core/http/endpoints/openai/chat.go"  caller.L=372 }
api-1  | Jul 15 13:43:26 DEBUG Options options=ContextSize:131072  Seed:1732589665  NBatch:512  F16Memory:true  MMap:true  NGPULayers:99999999  Threads:16  FlashAttention:"on"  Options:"use_jinja:true"  Options:"parallel:2"  Options:"cache_ram:4096"  Options:"kv_unified:true"  Options:"cache_idle_slots:true"  Options:"n_threads_batch:3"  Options:"threads:2"  Options:"n_threads:1"  Options:"cache_reuse:256"  Options:"spec_type:draft-mtp"  Options:"spec_n_max:6"  Options:"spec_p_min:0.75"  CacheTypeKey:"q8_0"  CacheTypeValue:"q8_0" caller={caller.file="/build/pkg/model/initializers.go"  caller.L=142 }
api-1  | Jul 15 13:43:28 DEBUG GRPC: Loading model with options options=Model:"llama-cpp/models/Qwen_Qwen3.5-2B-Q4_K_M.gguf"  ContextSize:131072  Seed:1732589665  NBatch:512  F16Memory:true  MMap:true  NGPULayers:99999999  Threads:16  ModelFile:"/models/llama-cpp/models/Qwen_Qwen3.5-2B-Q4_K_M.gguf"  FlashAttention:"on"  ModelPath:"//models"  Options:"use_jinja:true"  Options:"parallel:2"  Options:"cache_ram:4096"  Options:"kv_unified:true"  Options:"cache_idle_slots:true"  Options:"n_threads_batch:3"  Options:"threads:2"  Options:"n_threads:1"  Options:"cache_reuse:256"  Options:"spec_type:draft-mtp"  Options:"spec_n_max:6"  Options:"spec_p_min:0.75"  CacheTypeKey:"q8_0"  CacheTypeValue:"q8_0" caller={caller.file="/build/pkg/model/initializers.go"  caller.L=173 }
api-1  | Jul 15 13:43:28 DEBUG GRPC stderr id="qwen_qwen3.5-2b-127.0.0.1:41445" line="0.01.998.220 I system info: n_threads = 16, n_threads_batch = 3, total_threads = 16" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 }
api-1  | Jul 15 13:43:28 DEBUG GRPC stderr id="qwen_qwen3.5-2b-127.0.0.1:41445" line="0.01.998.255 I system_info: n_threads = 16 (n_threads_batch = 3) / 16 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | " caller={caller.file="/build/pkg/model/process.go"  caller.L=219 }
```


**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a23fcc90c36b49439a1a3bd785f8854c1816021e`.  There
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
{"case_id": "mudler_LocalAI__10845__a23fcc9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
