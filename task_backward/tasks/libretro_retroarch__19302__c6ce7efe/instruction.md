# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash on Gentoo and Ryzen 9

### Is there an existing issue for this?

- [x] This is a bug in RetroArch frontend
- [x] I have searched the existing issues

### Description

Retroarch segfaults immediately after launching. 

### Expected behavior

Retroarch should start normally

### Steps to reproduce the bug

1. 
2. `git clean -fdx && ./configure --enable-systemd --enable-dbus --enable-freetype --enable-pulse --enable-sse --enable-vulkan --enable-threads --enable-spirv_cross --enable-qt --enable-flac --enable-v4l2 --enable-al --enable-zlib --enable-alsa --enable-x11 --enable-sdl2 && make -j16`
3. `./retroarch`

### Version/Commit



### Bisect Results



### Present in the nightly version

I don't know

### Platform & operating system

Gentoo Linux amd64

### Affected Cores

_No response_

### Environment information

KDE Plasma 6.6.5
Qt 6.11.1
Wayland

### Relevant log output
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `556283a6689ab5502ceec86f4e83e8b8d796bbd8` and the full history behind it is present.
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
