# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Achievements crash 3DS console



## Description

When achievements trigger console will crash.

### Expected behavior

Achievement will trigger and banner will pop up. 

### Actual behavior

When an achievement triggers, 3DS will crash and show Luma error dump. 

### Steps to reproduce the bug

1. Play game with achievements enabled (Devil Crush for Turbographx 16 was one I could reliably reproduce this crash on)
2. Trigger an achievement. 
3. 3DS will crash and pop up error screen. 

### Version/Commit
You can find this information under Information/System Information

- RetroArch: 1.9.11

### Environment information

- OS: Latest 3DS update installed.
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `1e1919b236ccc17ce2302ed85bada21c040b9223` and the full history behind it is present.
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
