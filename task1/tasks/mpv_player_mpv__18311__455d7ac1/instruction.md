# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
regression master: cover art not displayed with ytdl_hook-thumbnails

### mpv Information

```bash
mpv v0.41.0-UNKNOWN Copyright © 2000-2026 mpv/MPlayer/mplayer2 projects
libplacebo version: v7.360.1
FFmpeg version: 8.1.2
FFmpeg library versions:
   libavcodec      62.28.102
   libavdevice     62.3.102
   libavfilter     11.14.102
   libavformat     62.12.102
   libavutil       60.26.102
   libswresample   6.3.102
   libswscale      9.5.102
```

### Other Information

```text
- Linux version:
NAME="Alpine Linux"
PRETTY_NAME="Alpine Linux v3.24"
- Kernel Version:
Linux yellow-orcess 7.1.4-0-stable #1-Alpine SMP PREEMPT_DYNAMIC 2026-07-18 16:32:59 x86_64 GNU/Linux
```

### Reproduction Steps

`mpv -v --no-config --script-opts-append=ytdl_hook-thumbnails=best  https://soundcloud.com/1odumdefect/imposter-2`


### Expected Behavior

Expect to see a video thumbnail, as with 0.41.0.


### Actual Behavior

But we see nothing, and even when forcing the window with `--force-window=immediate`, we have to `_` to display the cover.

### Log File

[output.log](https://github.com/user-attachments/files/30462836/output.log)

### Sample Files

_No response_

### I carefully read all instruction and confirm that I did the following:

- [x] I tested and confirmed that the issue exists with the [latest release version](https://github.com/mpv-player/mpv/releases/latest) or newer.
- [x] I provided all required information including system and mpv version.
- [x] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [x] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [x] I attached the full, untruncated log file.
- [x] I attached the backtrace in the case of a crash.



cc @guidocella
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `48e6c35c0e056d9e4ff04b98e012416697736d8a` and the full history behind it is present.
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
