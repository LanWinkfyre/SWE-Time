# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
gRPC backend crashes with GPF on AMD gfx1151 (Strix Halo APU) while stock llama.cpp works

**Disclaimer: I'm not an LLM/GPU expert at all, so I used AI (Claude Opus 4.6) to debug and collect data. I've done an initial evaluation and the thrust of the analysis seems reasonable, but apologies  in advance if I missed something.**


### Summary

The `llama-cpp` gRPC backend crashes with a general protection fault in `libamdhip64.so.7.2.70201` on AMD Strix Halo (gfx1151) during the first GPU compute dispatch. Stock llama.cpp (`llama-cli` and `llama-server`) works perfectly on the same hardware, same ROCm, same Docker container.

### Environment

- **Hardware**: AMD Ryzen AI MAX+ 395 w/ Radeon 8060S (gfx1151), 128GB DDR5, 32GB VRAM (UMA)
- **OS**: Ubuntu 24.04 LTS
- **Kernel**: `6.17.0-1017-oem` (installed via `linux-oem-24.04c`)
- **ROCm**: 7.2.1 (installed via `amdgpu-install --usecase=rocm --no-dkms`)
- **LocalAI**: upstream master @ `84870586`
- **llama.cpp**: `fae3a28070fe4026f87bd6a544aba1b2d1896566` (as vendored by LocalAI)
- **Backend built with**: `rocm/dev-ubuntu-24.04:7.2.1`, `BUILD_TYPE=hipblas`, `AMDGPU_TARGETS=gfx1151`

### What works vs what crashes

| Scenario | Binary | GPU Offload | Result |
|---|---|---|---|
| Stock `llama-cli` on host | `ggerganov/llama.cpp` | `ngl 10` | **PASS** — 268 t/s prompt, 82 t/s gen |
| Stock `llama-cli` inside Docker | `ggerganov/llama.cpp` | `ngl 10` | **PASS** — 263 t/s prompt, 83 t/s gen |
| Stock `llama-server` inside Docker | `ggerganov/llama.cpp` | `ngl 10` | **PASS** — 248 t/s prompt, 82 t/s gen |
| LocalAI gRPC `llama-cpp-fallback` | LocalAI `grpc-server.cpp` | `ngl 10` | **CRASH** — GPF in `libamdhip64.so` |
| LocalAI gRPC `llama-cpp-fallback` | LocalAI `grpc-server.cpp` | `ngl 0` (CPU) | **CRASH** — same GPF |
| HIP test (hipBLAS SGEMM/HGEMM) | custom test program | GPU compute | **PASS** |

### Crash details

The backend process crashes with a **general protection fault** inside the HIP runtime library. The crash is consistent and reproducible — always at the same offset.

**Kernel log:**
```
traps: grpcpp_sync_ser[619967] general protection fault ip:7ef567c999df sp:7ef3ed7e39d0 error:0 in libamdhip64.so.7.2.70201[2b09df,7ef567a0c000+481000]
amdgpu: Freeing queue vital buffer 0x..., queue evicted
```

**Crash point in LocalAI logs:**

The gRPC backend successfully completes all these steps:
1. HIP device initialization: `ggml_cuda_init: found 1 ROCm devices: Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32`
2. Model tensor loading: `load_tensors: offloaded 10/17 layers to GPU`
3. GPU VRAM allocation: `ROCm0 model buffer size = 521.18 MiB`
4. KV cache allocation: `ROCm0 KV buffer size = 36.00 MiB`
5. Compute graph reservation: `sched_reserve: ROCm0 compute buffer size = 254.50 MiB`
6. Graph planning: `sched_reserve: graph nodes = 503, graph splits = 87 (with bs=512), 2 (with bs=1)`
7. `srv load_model: initializing slots, n_slots = 1`
8. **CRASH** — process exits with GPF, gRPC connection EOF

The crash happens during slot initialization, which is the first actual GPU kernel dispatch.

### Reproduction

**Working (stock llama-server inside Docker):**
```bash
# Build llama.cpp with ROCm
cd llama.cpp # https://github.com/ggerganov/llama.cpp @ 408225bb1a63faef725685515cfe583fcc964d09
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc) --target llama-server

# Run in Docker with GPU
docker run --rm -p 8080:8080 \
  --device /dev/kfd --device /dev/dri \
  --group-add video --group-add $(stat -c '%g' /dev/dri/renderD128) \
  -v $(pwd)/build/bin:/native:ro \
  -v /path/to/model.gguf:/model.gguf:ro \
  -v /opt/rocm:/opt/rocm:ro \
  -e HSA_OVERRIDE_GFX_VERSION=11.5.1 \
  -e ROCBLAS_TENSILE_LIBPATH=/opt/rocm/lib/rocblas/library \
  --entrypoint /bin/sh ubuntu:24.04 -c '
    export LD_LIBRARY_PATH=/native:/opt/rocm/lib:/opt/rocm/lib64:/opt/rocm/llvm/lib
    /native/llama-server -m /model.gguf -ngl 10 -c 2048 --host 0.0.0.0 --port 8080
  '
# Result: works at 248 t/s prompt, 82 t/s generation
```

**Crashing (LocalAI gRPC backend):**
```bash
# Build LocalAI backend with ROCm 7.2.1
docker buildx build -f backend/Dockerfile.llama-cpp \
  --build-arg BUILD_TYPE=hipblas \
  --build-arg BASE_IMAGE=rocm/dev-ubuntu-24.04:7.2.1 \
  --build-arg GRPC_BASE_IMAGE=ubuntu:24.04 \
  --build-arg CMAKE_ARGS="-DAMDGPU_TARGETS=gfx1151" \
  --platform linux/amd64 --output type=docker \
  -t localai-backend-rocm7:latest .

# Use it in an AIKit/LocalAI model image and run:
docker run --rm -p 8080:8080 \
  --device /dev/kfd --device /dev/dri \
  --group-add video --group-add $(stat -c '%g' /dev/dri/renderD128) \
  -e LOCALAI_FORCE_META_BACKEND_CAPABILITY=amd \
  -e HSA_OVERRIDE_GFX_VERSION=11.5.1 \
  my-localai-model

# Result: GPF in libamdhip64.so.7.2.70201 at offset +0x2b09df
```

### Analysis

The only difference between the working and crashing scenarios is the **LocalAI gRPC server wrapper** (`backend/cpp/llama-cpp/grpc-server.cpp`). The same llama.cpp version, same ROCm libraries, same Docker container, same model — stock llama.cpp binaries work while the gRPC-wrapped version crashes.

Key differences in the gRPC wrapper vs stock llama.cpp:
1. **gRPC thread pool**: `BuildAndStart()` spawns worker threads before any HIP initialization
2. **Model loading on worker thread**: `LoadModel` RPC handler calls `llama_backend_init()` and model loading on a gRPC worker thread
3. **Static gRPC linkage**: The backend statically links gRPC which may interfere with HIP's signal handling or memory management
4. **Process name**: Kernel identifies the process as `grpcpp_sync_ser` (gRPC synchronous server)

In stock llama.cpp, all GPU initialization and inference happen on the main thread or a single controlled worker thread. The gRPC wrapper introduces multi-threaded context that appears to conflict with HIP's runtime on gfx1151.

### Things I've already tried that did NOT fix it

- Moving `llama_backend_init()` and `common_init()` to `main()` before `BuildAndStart()`
- Adding explicit `ggml_backend_dev_get()` GPU enumeration on main thread before gRPC starts
- Disabling fit (`fit:false` option)
- Disabling warmup (`warmup:false` option)
- Using host ROCm libraries via bind mount instead of bundled ones
- Bypassing the bundled `ld.so` dynamic linker
- Different model architectures (Llama, GraniteHybrid) — same crash
- Different VRAM sizes (512MB, 32GB) — same crash pattern after fixing OOM

### Suggested investigation areas

1. Does gRPC's thread pool / signal handling conflict with HIP's context management?
2. Is there a gRPC build flag that could avoid this (e.g., async server instead of sync)?
3. Could the static linkage of gRPC interfere with `libamdhip64.so`'s dynamic initialization?
4. On other ROCm GPUs (gfx1100, gfx90a), does the gRPC backend work? This might be gfx1151-specific due to stricter HIP context requirements on APUs.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ad742738cb4abba825e2f67447acd6774d82e8d9`.  There
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
{"case_id": "mudler_LocalAI__9374__ad74273",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
