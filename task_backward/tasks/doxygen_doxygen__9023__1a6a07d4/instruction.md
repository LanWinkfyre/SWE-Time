# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
markdown bold and ref

**Describe the bug**
In markdown source, if a ref to a page is used inside a bold line, the resulting dox is not bold.

**Expected behavior**
using \ref should not break markdown bold typesetting 

**Screenshots**

![Screenshot from 2022-01-11 11-53-57](https://user-images.githubusercontent.com/11328509/148929941-04710f13-dbc5-4ec0-a79c-712028834584.png)

**To Reproduce**
Run doxygen for attached file [Test.zip](https://github.com/doxygen/doxygen/files/7845878/Test.zip)

**Version**
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `1f1ac2838cfcc8e4bd95501df4d7376d35a0848e` and the full history behind it is present.
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
