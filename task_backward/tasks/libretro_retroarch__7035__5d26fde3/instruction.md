# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash on gnome3 wayland (with bisect)

# First and foremost consider this:
- Only RetroArch bugs should be filed here. Not core bugs or game bugs
- This is not a forum or a help section, this is strictly developer oriented

## Description

A recent crash on just starting retroarch on weston/wayland gnome3 crashes with:

```
i30817@AIVAS:~$ retroarch 
listener function for opcode 5 of wl_keyboard is NULL
Aborted
```

### Expected behavior

### Actual behavior

### Steps to reproduce the bug

### Bisect Results


### Version/Commit
You can find this information under Information/System Information

(this is the local version installed from the ppa not my built one)

- RetroArch: 

Compiler: GCC (7.3.0) 64-bitBuilt: Jul 30 2018



### Environment information

- OS: Linux AIVAS 4.15.0-29-generic #31-Ubuntu SMP Tue Jul 17 15:39:52 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
- Compiler: gcc (Ubuntu 7.3.0-16ubuntu3) 7.3.0
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `bdf5efd4ab162f8d3d50029b3f9a79fc56578c07` and the full history behind it is present.
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
