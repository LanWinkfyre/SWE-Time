# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Default keybinds for lightgun are missing

## Description

The zapper is broken in RetroArch as experienced in cores like `fceumm` and `nestopia` and the game `Duck Hunt`. Basically RetroArch does not register any clicks from the mouse and the zapper never fires. This affects all input drivers and other cores and games are possibly affected.

Also see this related core issue: https://github.com/libretro/nestopia/issues/49

And these issues may be related? 

https://github.com/libretro/RetroArch/issues/8324
https://github.com/libretro/RetroArch/issues/7697

### Expected behavior

Mouse clicks should be registered by the zapper.

### Actual behavior

RetroArch does not register any mouse clicks when using the zapper.

### Steps to reproduce the bug

1. Start `nestopia` and the game `Duck Hunt` with a mouse connected.
2. Observe that the mouse can control the crosshair, but mouse clicks do nothing and the zapper is rendered unplayable.

### Bisect Results










### Version/Commit
You can find this information under Information/System Information



### Environment information

- OS: `Slackware64-current`
- Compiler: `clang-8.0.0`
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `3064d0d441bfcd2a13ff46a1a813f6c7339c4c24` and the full history behind it is present.
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
