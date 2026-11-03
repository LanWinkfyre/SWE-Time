# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Eval bug: Qwen Models segfault on Vulkan

### Name and Version

./llama-cli --version
ggml_vulkan: Found 1 Vulkan devices:
ggml_vulkan: 0 = AMD Radeon Graphics (RADV REMBRANDT) (radv) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 32 | shared memory: 65536 | int dot: 1 | matrix cores: none

built with cc (Ubuntu 11.4.0-1ubuntu1~22.04.2) 11.4.0 for x86_64-linux-gnu

### Operating systems

Linux

### GGML backends

Vulkan

### Hardware

Radeon 680M

### Models

Qwen3-Coder:30A3B, Qwen3:4B, Qwen2.5-Coder:1.5b

### Problem description & steps to reproduce

All of those models segfault when loading them. some of them give a message of an invalid pointer





### Relevant log output
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `4abef75f2cf2eee75eb5083b30a94cf981587394` and the full history behind it is present.
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
