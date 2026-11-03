# Locate the commit that introduced this regression

A regression was reported against `Comfy-Org/ComfyUI`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Description

Expected Behavior


Actual Behavior
The second sampling pass hangs indefinitely at 0%|0/2 with no progress, no error output, and GPU utilization drops to 0% (12W idle power). The process must be manually interrupted. The first pass completes normally every time.

Steps to Reproduce
Hardware: NVIDIA GB10 (DGX Spark) — unified memory architecture, 121 GB shared VRAM/RAM
Start ComfyUI with flags: --normalvram --disable-dynamic-vram --reserve-vram 1 --disable-pinned-memory --use-sage-attention --force-fp16 --bf16-unet --bf16-vae --bf16-text-enc --dont-upcast-attention --disable-mmap
Run a two-pass WanVideo i2v workflow:
Pass 1: load Wan2.2 14B transformer + Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16, sample 2 steps (timesteps 1000→941)
Pass 2: reload same transformer + Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16, sample 2 steps (timesteps 803→60)
Pass 1 completes in ~3 minutes. Pass 2 starts loading the transformer, reaches Sampling start, prints Generated new RoPE frequencies, then hangs at 0%|0/2 indefinitely.
Bisection Result
Commit	Result




Root Cause Analysis



Environment
OS: Ubuntu 24.04 (Linux 6.17.0-1014-nvidia, aarch64)
Hardware: NVIDIA GB10 (DGX Spark), unified memory 121 GB
CUDA: 13.0 / Driver 580.142
PyTorch: 2.12.0+cu130

SageAttention: 2.2.0 (compiled for sm_121)
Custom node: ComfyUI-WanVideoWrapper (kijai)
Workaround
```

## What you have

- `/testbed/repo` is a git clone of `Comfy-Org/ComfyUI` truncated just after the regression was
  reported.  `HEAD` is `04856acc699f1559a11e00a9f68d2f9f9b9b8e96` and the full history behind it is present.
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
