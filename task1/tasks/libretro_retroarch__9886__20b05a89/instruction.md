# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ffmpeg build issue on Linux

## Description

Build fails due to the ffmpeg core starting today

### Expected behavior

Build succeeds

### Actual behavior

```
cores/libretro-ffmpeg/video_buffer.c: In function ‘video_buffer_create’:
cores/libretro-ffmpeg/video_buffer.c:73:25: error: ‘video_decoder_context_t {aka struct video_decoder_context}’ has no member named ‘hw_source’; did you mean ‘source’?
           !b->buffer[i].hw_source ||
                         ^~~~~~~~~
                         source
Makefile:211: recipe for target 'obj-unix/release/cores/libretro-ffmpeg/video_buffer.o' failed
```

### Steps to reproduce the bug

1. Pull Retroarch source
2. ./configure && make clean && make -j5

### Bisect Results



### Environment information

- OS: Linux Mint 19.3
- Compiler: GCC 7.4.0 64-bit
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `e5a651789730ed5c9afcf60514e6fd2e8b308588` and the full history behind it is present.
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
