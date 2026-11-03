# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
1.10 regression: partition errors out on empty input

maintenance/1.9.x:

```
In [8]: ap = np.array([0, 2, 4, 6, 8, 10])

# Passing an empty 'k' array to partition is a no-op:
In [9]: ap.partition(np.array([], dtype=np.int64))

In [10]: ap
Out[10]: array([ 0,  2,  4,  6,  8, 10])
```

1.10.1:

```
In [2]: ap = np.array([0, 2, 4, 6, 8, 10])

In [3]: ap.partition(np.array([], dtype=np.int64))
---------------------------------------------------------------------------
MemoryError                               Traceback (most recent call last)
<ipython-input-3-c708b3f943a6> in <module>()
----> 1 ap.partition(np.array([], dtype=np.int64))

MemoryError: 
```

Noticed this because it's breaking some tests in patsy.


`git bisect` says:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `3390e440ef3563cf87eeea66ea672f8e5a6a8665` and the full history behind it is present.
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
