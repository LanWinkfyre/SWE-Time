# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
clBLAST support broken





```
llm_load_tensors: ggml ctx size =    0.12 MiB
llm_load_tensors: using OpenCL for GPU acceleration
llm_load_tensors: mem required  =  205.19 MiB
llm_load_tensors: offloading 32 repeating layers to GPU
llm_load_tensors: offloading non-repeating layers to GPU
llm_load_tensors: offloaded 33/33 layers to GPU
llm_load_tensors: VRAM used: 5461.02 MiB
...................................................................................................
llama_new_context_with_model: n_ctx      = 512
llama_new_context_with_model: freq_base  = 10000.0
llama_new_context_with_model: freq_scale = 1
llama_new_context_with_model: KV self size  =   64.00 MiB, K (f16):   32.00 MiB, V (f16):   32.00 MiB
llama_build_graph: non-view tensors processed: 676/676
llama_new_context_with_model: compute buffer total size = 76.32 MiB
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
GGML_ASSERT: ggml.c:7765: ggml_are_same_shape(src0, src1)
llama.sh: line 17:  1461 Aborted                 (core dumped) ./main --threads ${NUM_CPUS} --n-gpu-layers ${MODEL_GPU_LAYERS} --model ./models/${MODEL} --temp ${MODEL_TEMP} --repeat_penalty 1.1764705882352942 --n-predict -1 --top_k 42 --top_p 0 -e ${MODEL_ARGS} --prompt "${MODEL_PROMPT}"
```

Originally reported in #4451 - but I realized this also applies to any model when I tried testing Intel Neural 7B v3-3.



cc @ggerganov
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `948ff137ec37f1ec74c02905917fa0afc9b97514` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
