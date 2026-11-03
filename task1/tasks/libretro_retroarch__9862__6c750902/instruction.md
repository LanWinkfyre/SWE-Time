# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Database entries display "Directory not found."

## Description

Database entries can't be viewed and give a "Directory not found." error. The game list in each database is still visible and scanning still functions.

### Expected behavior

Games in databases can be viewed.

### Actual behavior

Games just show "Directory not found."

### Steps to reproduce the bug

1. Start retroarch.
2a. Navigate to Main Menu > Information > Database Manager.
3a. Open any database and select a game from the list.

2b. Navigate to any database-matched playlist entry.
3b. Open Information > Database Entry.

### Bisect Results


(had to overwrite ffmpeg_core.c with a newer version to compile most stages of the bisect)

### Version/Commit



### Environment information

- OS: Linux Mint 19.2
- Compiler: GCC 7.4.0 64-bit
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `e9a264217a48b809b1dce65582ee063e33f7093a` and the full history behind it is present.
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
