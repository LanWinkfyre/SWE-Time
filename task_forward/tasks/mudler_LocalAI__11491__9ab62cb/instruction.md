# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Parakeet Metal backend builds without Metal support on macOS

## Problem

The Darwin build matrix builds `parakeet-cpp` with `BUILD_TYPE=metal`, but the
Parakeet Makefile does not pass `PARAKEET_GGML_METAL=ON` to CMake. The build
succeeds, but the resulting backend is CPU-only despite being published as a
Metal backend.

## Reproduce

On an Apple Silicon Mac:

```sh
make protogen-go
BUILD_TYPE=metal make -C backend/go/parakeet-cpp parakeet-cpp-grpc
otool -L backend/go/parakeet-cpp/libparakeet.dylib
```

The resulting library links Accelerate but does not link Metal or MetalKit.

## Fix

Add the missing Metal build mapping to `backend/go/parakeet-cpp/Makefile`:

```make
else ifeq ($(BUILD_TYPE),metal)
	CMAKE_ARGS+=-DPARAKEET_GGML_METAL=ON
```

## Result

After rebuilding, the library links Metal and MetalKit and selects the Apple M1
GPU at runtime. Using the same five-minute audio and Parakeet TDT 0.6B v3 FP16
model, transcription time dropped from 82.57 seconds to 50.18 seconds with a
byte-identical response.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9ab62cbb3834db1edf4eb455d0e4a6d474385470`.  There
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
{"case_id": "mudler_LocalAI__11491__9ab62cb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
