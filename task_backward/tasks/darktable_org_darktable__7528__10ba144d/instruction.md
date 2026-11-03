# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dt master crashing when using color calibration module

**Describe the bug**
dt crashes when using the "color calibration" module


**To Reproduce**
1. Open an image in darkroom
2. Use either one of the sliders in the "grey tab" or select on of the b&w film simulations
3. dt immediately becomes unresponsive and crashes after a short time

**Expected behavior**
not crashing :-)


**Platform**
 - Darktable master
 - OS: Fedora 33, Intel
 - no cl on this machine

**Additional context**
starting on console gives various hints

```
Using cmatrix codepath
malloc(): unaligned tcache chunk detected

(darktable:74518): Gtk-WARNING **: 23:06:12.110: Failed to set text '<markup>' from markup due to error parsing markup: Error on line 1 char 28: Document ended unexpectedly with elements still open ? ?markup? was the last element opened
Abgebrochen (Speicherabzug geschrieben)
```

or
```
(darktable:74817): Gtk-WARNING **: 23:09:08.096: Failed to set text 'R\xb6\u0004\u0008!\u007f' from markup due to error parsing markup: Error on line 1 char 26: Invalid UTF-8 encoded text in name ? not valid ?color ca\xd0\u0008?

(darktable:74817): Gtk-WARNING **: 23:09:08.096: Failed to set text 'R\xb6\u0004\u0008!\u007f' from markup due to error parsing markup: Error on line 1 char 19: Invalid UTF-8 encoded text in name ? not valid ?\xd0\u0008?
malloc_consolidate(): unaligned fastbin chunk detected
Abgebrochen (Speicherabzug geschrieben)
```

bisecting gave:
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `f755cfc283773cc084495006bdf5a31c17ae4ff1` and the full history behind it is present.
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
