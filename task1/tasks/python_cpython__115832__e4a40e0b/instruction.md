# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
# Bug report

### Bug description:

Coverage.py runs its test suite against nightly builds of Python.  The tests stalled last night.  Running them locally, there's one test that freezes the suite.  The GitHub action is eventually cancelled by timing out after six hours: https://github.com/nedbat/coveragepy/actions/runs/8000886484






To reproduce:

and there it is stuck.

### CPython versions tested on:

CPython main branch

### Operating systems tested on:

Linux, macOS

<!-- gh-linked-prs -->
### Linked PRs
* gh-115856
<!-- /gh-linked-prs -->
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `17dab2e572141a4295325bf7019301fece301fe1` and the full history behind it is present.
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
