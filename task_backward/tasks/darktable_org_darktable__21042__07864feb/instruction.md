# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
IOP: huge regression in overlay last night

```
Test 0160-overlay
      Image mire1.cr2
      Timing cpu 4.35s
      Expected CPU vs. current CPU report :
      ----------------------------------
      Max dE                   : 89.61576
      Avg dE                   : 4.48558
      Std dE                   : 9.59455
      ----------------------------------
      Pixels below avg + 0 std : 76.92 %
      Pixels below avg + 1 std : 86.90 %
      Pixels below avg + 3 std : 96.89 %
      Pixels below avg + 6 std : 99.99 %
      Pixels below avg + 9 std : 100.00 %
      ----------------------------------
      Pixels above tolerance   : 24.55 %
 
  FAILS: image visually changed

Test 0161-overlay-modules-before-after
      Image mire1.cr2
      Timing cpu 5.23s
      Expected CPU vs. current CPU report :
      ----------------------------------
      Max dE                   : 96.63399
      Avg dE                   : 6.40898
      Std dE                   : 13.12593
      ----------------------------------
      Pixels below avg + 0 std : 76.79 %
      Pixels below avg + 1 std : 84.49 %
      Pixels below avg + 3 std : 97.33 %
      Pixels below avg + 6 std : 100.00 %
      Pixels below avg + 9 std : 100.00 %
      ----------------------------------
      Pixels above tolerance   : 24.87 %
 
  FAILS: image visually changed
```

@jenshannoschwalm : can you have a look? TIA.

The bisect gives me:
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `92e04f41a6595b3fd2df3bcc1a6bb70ea12f807b` and the full history behind it is present.
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
