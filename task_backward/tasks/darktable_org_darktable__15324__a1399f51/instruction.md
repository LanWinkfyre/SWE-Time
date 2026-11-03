# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Rotation & Perspective - Regression

To reproduce:
1. Open any image
2. Select Rotation & Perspective
3. Have selected on of the automatic crop option (say original format)
4. Do manual or automatic detection
5. Apply the vertical / horizontal or both adjustments
6. Collapse the module
7. See that the crop is not applied and the black borders are still displayed
8. Expand the module again, and see that the crop indicator overlay is not properly placed on the picture (which is expected given point 7 above).
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `76cf661582f38e518e29a1b44ffce93865151917` and the full history behind it is present.
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
