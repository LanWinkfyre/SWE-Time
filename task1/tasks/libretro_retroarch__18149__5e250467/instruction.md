# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Is there an existing issue for this?

- [x] This is a bug in RetroArch frontend
- [x] I have searched the existing issues

### Description

Tested with A Link to the Past and Secret of Evermore with bsnes-mercury Core:

Starting a Archipelago Multiworld Seed with those Games results in a Segmentation Fault which crashes Retroarch. 
Without running Archipelago (and the SNI-Interface) Retroarch doesn't crash but you could obviously not participate in the Multiworld in this State

### Expected behavior

_No response_

### Steps to reproduce the bug

1. 
2. Start Archipelago and create a Multiworld Seed
3. Try to play the Seed
4. Observe Retroarch crashing with a segmentation fault

### Version/Commit



### Bisect Results



### Present in the nightly version

Yes, this is reproduced in the nightly build

### Platform & operating system

Arch Linux

### Affected Cores

_No response_

### Environment information

_No response_

### Relevant log output

```shell

```
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `e3435221d8ffa4b69ec013658151a64d0d8fa83a` and the full history behind it is present.
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
