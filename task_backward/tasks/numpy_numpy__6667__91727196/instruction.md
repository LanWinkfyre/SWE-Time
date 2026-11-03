# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ma.make_mask handles ma.nomask input incorrectly.

This was a nasty little bug to chase down. I suspect `ma.mask_or` is not alone in this.



Whereas

```
In [1]: np.__version__
Out[1]: '1.9.2'

In [2]: m = ma.mask_or(ma.nomask, ma.nomask, shrink=False)

In [3]: m
Out[3]: False

In [4]: m is ma.nomask
Out[4]: True
```
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `1d511429ac04d137c3d9ec7da9160bec7baa2829` and the full history behind it is present.
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
