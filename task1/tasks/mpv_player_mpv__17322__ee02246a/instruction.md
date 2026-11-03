# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
0.41:gpu-next/vulkan reports unusually high contrast for SDR content/display

### mpv Information

```bash
mpv v0.41.0 Copyright © 2000-2025 mpv/MPlayer/mplayer2 projects
 built on Dec 22 2025 14:58:51
libplacebo version: v7.351.0
FFmpeg version: n8.0.1
FFmpeg library versions:
   libavcodec      62.11.100
   libavdevice     62.1.100
   libavfilter     11.4.100
   libavformat     62.3.100
   libavutil       60.8.100
   libswresample   6.1.100
   libswscale      9.1.100
```

### Other Information

```text
also on git master+placebo master
```

### Reproduction Steps

on 0.41:
```mpv --no-config --gpu-api=vulkan``` => video-target-params.min_luma = 1e-6
```mpv --no-config --gpu-api=opengl``` => video-target-params.min_luma = 0.203

on 0.40, they are both 0.203.



### Expected Behavior

```auto is the default and assumes 1000:1 contrast as a typical  SDR display```

### Actual Behavior

na

### Log File

[log.txt](https://github.com/user-attachments/files/24842234/log.txt)

### Sample Files

_No response_

### I carefully read all instruction and confirm that I did the following:

- [x] I tested with the latest mpv version to validate that the issue is not already fixed.
- [x] I provided all required information including system and mpv version.
- [x] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [x] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [x] I attached the full, untruncated log file.
- [x] I attached the backtrace in the case of a crash.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `e99a9168c1d11bddf0530c69f578ce2a5b7d0b8f` and the full history behind it is present.
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
