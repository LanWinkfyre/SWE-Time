# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
The "Hotkey Enable Delay" feature breaks when "All Users Control Menu" is enabled

## Description

When "All Users Control Menu" is enabled, the "Hotkey Enable Delay" feature breaks, it only works when set to "0", any other value never blocks the input from being passed to the core.
And even at "0" it doesn't always work properly, if you spam the hotkey it sometimes still sends the input to the core.

### Expected behavior

If set to anything but "0", the inputs sent to the core should be blocked after that number of frames.

### Actual behavior

Unless it's set to "0", the inputs will keep getting sent to the core.

### Steps to reproduce the bug

1. Turn ON `Settings > Input > Menu Controls > All Users Control Menu`
2. Set a "Hotkey Enable" hotkey in `Settings > Input > Hotkeys` to Select.
3. Set "Hotkey Enable Delay" to anything but "0".
4. Boot a game.
5. Hold Select and notice that you can still move.

### Bisect Results



### Version/Commit



### Environment information

- OS: tested on Windows 10 and on a Linux Mint VM
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `212013f67712f2342abfd2d585c30435e8839ae6` and the full history behind it is present.
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
