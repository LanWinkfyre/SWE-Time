# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Segfault on rgui and ozone, NOT xmb

## Description
Retroarch crashes with segfault on ozone and rgui drivers when starting any core content if there exists at least 1 playlist.
I DO NOT have this problem with XMB driver.
This happens on Intel graphics chipset. No issues at all with Nvidia graphics!

### Expected behavior
No crash

### Actual behavior

Crash

### Steps to reproduce the bug

Grab an Intel Graphics Notebook (like me it's Intel Graphics 3000 and 5500), create at least 1 playlist and run. It will segfault with any driver except XMB!

### Bisect Results

Since first use

### Version/Commit
v1.9.0

### Environment information

- OS: Arch Linux Kernel 5.8.7
- Compiler: -


Hm I'm not sure it's related since it even crashes with XMB for me, and I'm using Linux Mint, but I get this:
```
[INFO] [X11]: Suspending screensaver (X11, xdg-screensaver).
X Error of failed request:  BadName (named color or font does not exist)
  Major opcode of failed request:  141 (RANDR)
  Minor opcode of failed request:  16 (RRCreateMode)
  Serial number of failed request:  15
  Current serial number in output stream:  15

=================================================================
==48898==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 1971 byte(s) in 1 object(s) allocated from:
    #0 0x7ff554f44bc8 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.5+0x10dbc8)
    #1 0x7ff5536eb84d  (/usr/lib/x86_64-linux-gnu/libXrandr.so.2+0x684d)

Direct leak of 88 byte(s) in 1 object(s) allocated from:
    #0 0x7ff554f44bc8 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.5+0x10dbc8)
    #1 0x7ff55399078a in pa_xmalloc (/usr/lib/x86_64-linux-gnu/libpulse.so.0+0x3b78a)

SUMMARY: AddressSanitizer: 2059 byte(s) leaked in 2 allocation(s).
```

I still get the 2nd LeakSanitizer thing (the one with libpulse I mean) with previous commits when I close RA, but no crash on content load.
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `60b26bd490915ee0bbf169324e8f570f14b9444b` and the full history behind it is present.
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
