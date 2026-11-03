# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
metal stablediffusion-ggml: shipped Metal library is missing `kernel_mul_mv_ext_bf16_f32_r1_5`, so every bf16 LTX-2 video model dies at pipeline compile

## Summary

The `latest-metal-darwin-arm64-stablediffusion-ggml` backend loads an LTX-2 video
model completely and correctly, then fails at Metal pipeline compilation because
a matrix-vector kernel is absent from the embedded Metal library. Every bf16
tensor in the model hits this. The result is that the ggml video path is
unusable on Apple Silicon.

Image generation through a different backend is unaffected.

## Environment

- LocalAI **4.7.1**
- Backend `metal-stablediffusion-ggml`, installed from
  `quay.io/go-skynet/local-ai-backends:latest-metal-darwin-arm64-stablediffusion-ggml`
- Backend digest `sha256:9cafbf0956c55791cac472f20c73f55f425eeaefeb9d9a9bb22c9c5b8e8d7258`
- macOS **26.5.2** (build 25F84), Apple **M3 Ultra**, 256 GB unified memory
- Model: `ltx-2.3-22b-distilled-Q4_K_M.gguf`, 13.34 GB, valid GGUF magic

## What works, which is almost everything

The failure is late, and worth describing precisely so it is clear the model and
the loader are fine:

- Full weight load, **28542.63 MB**, all five weight files
- Metal initialisation clean, reporting **`has bfloat = true`**
- `Version: LTXAV` detected correctly
- Euler sampler and LTX2 scheduler selected
- Prompt tokenized, the gemma text encoder's **626 tensors loaded in 3.53 s**

It then dies at `ltxav_text_projection`, immediately after the bf16
`embeddings_connectors`.

## The failure

```
compiling pipeline: kernel_mul_mv_ext_bf16_f32_r1_5
[ERROR] MTLLibraryErrorDomain Code=5 "Function kernel_mul_mv_ext_bf16_f32_r1_5
        was not found in the library"
SIGSEGV: segmentation violation, signal arrived during cgo execution
```

The `SIGSEGV` is a separate defect, filed alongside this one as *"stablediffusion-ggml
backend segfaults instead of returning an error when a Metal pipeline fails to
compile"* (companion issue: #BBB). This report is only about the missing function.

## The kernel is matrix-VECTOR, not matrix-matrix

Worth stating because it is easy to misread. The missing symbol is
`kernel_mul_mv_ext_bf16_f32_r1_5`: `mv`, matrix-vector. The matrix-matrix
equivalent `kernel_mul_mm_bf16_f32` **is** present and compiles successfully
earlier in the same run. A build that ships one and not the other looks like an
incomplete kernel-generation matrix rather than a deliberate omission.

## Please do not verify this with `strings`, it gives the wrong answer

We lost time to this and it seems worth passing on.

`strings libgosd-fallback.so | grep kernel_mul_mv_ext_bf16_f32_r1_5` returns a
hit, which reads as "the kernel is present". It is not evidence of that. The
shared object embeds the Metal shader **source** as text, plus a printf-style
name template:

```
kernel_mul_mv_ext_%s_%s_r1_%d
void kernel_mul_mv_ext_q4_f32_impl(
kernel void kernel_mul_mv_ext_q4_f32_disp(
```

So `strings` is matching source text and generated name fragments, not the
compiled library's function table. Only Metal's own
`MTLLibraryErrorDomain Code=5` at pipeline-compile time settles whether a
function is actually in the library.

## What would help

1. Confirm whether `kernel_mul_mv_ext_bf16_f32_r1_5` is expected in this build.
   Sibling ranks `r1_2`, `r1_3` and `r1_4` appear alongside it in the same name
   list, so if those are present and `r1_5` is not, the kernel-generation matrix
   is likely just short one entry.
2. If it is a build-matrix gap, a rebuilt backend image is all that is needed;
   there is nothing to change on the model side.

## Notes

- `local-ai backends install` does **not** fix this. We compared the release and
  master backend builds and `libgosd-fallback.so` is byte-identical between them
  (`sha256:0b1317ee…`), so pulling the other channel installs the same library.
- Happy to run diagnostics on request. The model and hardware stay available
  specifically to re-test after any backend rebuild.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `44413a9d06bf5bc52ce088ba8ca74e5a2e8bee26`.  There
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
{"case_id": "mudler_LocalAI__11530__44413a9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
