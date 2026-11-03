# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Eval bug: MedGemma-27B-it-IQ3-XS no longer fitting in 16GB card (RTX 2000E Ada)

### Name and Version



### Operating systems

Linux

### GGML backends

Vulkan, CUDA

### Hardware

AMD EPYC 4545P + RTX2000E Ada Gen.

### Models

MedGemma 27B-it-IQ3-XS

### Problem description & steps to reproduce

Hi, I'm using `llama-server` to self host a MedGemma model (https://huggingface.co/unsloth/medgemma-27b-it-GGUF) but recent changes don't allow me to load the IQ3-XS quant on my 16GB Card (RTX2000E Ada). Model fails to load with memory allocation errors using CUDA and Vulkan.







### Relevant log output
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `e1f15b454fbadfddf8f1ec450bf6d390d9db7adb` and the full history behind it is present.
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
