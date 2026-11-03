# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Infinite loop of setting/unsetting fullscreen in wayland

### mpv version and platform
mpv git master and sway (1.2-ba8586e2)

### Reproduction steps
Play any video and use sway's keybindings for making a client fullscreen (default: `super+f`). Using mpv's fullscreen keybind (`f`) works normally.

### Expected behavior
mpv goes fullscreen

### Actual behavior
mpv rapidly goes in and out of fullscreen without stopping. Pressing `super+f` again makes it stop. Curiously, pressing `f` (or whatever mpv's fullscreen keybinding is for you) doesn't stop the going in/out of fullscreen behavior but instead just makes it go slower.

### Log file
https://0x0.st/zlHC.txt

This is probably a wayland only thing (at least i3 didn't have this problem). No idea if a similar thing happens in other compositors that have their own fullscreen commands. Something to do with the window state stuff probably caused this and/or exposed a flaw in the wayland code.

 I probably can fix this along with the VOCTRL and window state stuff in wayland common.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `78f1629a539cc14a598831a73c59c3763c074094` and the full history behind it is present.
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
