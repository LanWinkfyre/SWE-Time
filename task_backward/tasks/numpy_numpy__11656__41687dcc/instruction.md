# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Cannot pickle numpy.datetime64 scalars in Python 3.6

### Reproducing code example:

Using `numpy==1.15.0` and Python 3.6

```
import pickle
import numpy as np
pickle.dumps(np.datetime64('2016-01-01T00:00:00.000000000'))
```

leads to `BufferError: could not get scalar buffer information`

### Numpy/Python version information:

```
>>> import sys, numpy; print(numpy.__version__, sys.version)
1.15.0 3.6.4 | packaged by conda-forge | (default, Dec 23 2017, 16:54:01)
[GCC 4.2.1 Compatible Apple LLVM 6.1.0 (clang-602.0.53)]
```
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `e14db2f4fcbcf030701a0410a1d647edfa5f0261` and the full history behind it is present.
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
