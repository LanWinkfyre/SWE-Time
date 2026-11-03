# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Editor selection is broken in SCM editor

Here's a recording demonstrating Insiders (left) and previous Stable 1.74 (right):

https://user-images.githubusercontent.com/22350/217783637-c155d3fe-7c8d-424f-b06c-4f2c16ed9b0a.mp4

Steps:

1. Open the SCM view and add a long line
2. Shorten the width of the side bar such that the text wraps

🐛 Notice how:

- When selecting the entire buffer, the selection expands beyond the text
- When selecting a subrange, sometimes the start position of the selection moves
- The rounded corners is generally broken: not all corners are rounded any more. This applies even for 1.74.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `89c4f61de26b4682d4de44c6c5f7801cf0f261cf` and the full history behind it is present.
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
