# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Error when importing NumPy main (No module named 'numpy.core._multiarray_umath')

### Describe the issue:

In NumPy main, when I do an inplace build, I can no longer import NumPy. I get

```
Traceback (most recent call last):
  File "./numpy/core/__init__.py", line 23, in <module>
    from . import multiarray
  File "./numpy/core/multiarray.py", line 10, in <module>
    from . import overrides
  File "./numpy/core/overrides.py", line 6, in <module>
    from numpy.core._multiarray_umath import (
ModuleNotFoundError: No module named 'numpy.core._multiarray_umath'
```

 

There are several errors in the build log, which I've included here https://gist.github.com/asmeurer/40754d1a4429449e1d558e003caa1860.

There seem to be some issues with the build scripts with C++. Perhaps they were never tested with clang? 

 

### Reproduce the code example:

```python
git clean -dfX
python setup.py build_ext --inplace
python -c 'import numpy'
```


### Error message:

_No response_

### NumPy/Python version information:

This is the latest NumPy main. I am using Python 3.9.2, on macOS.
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `c280e21a74f2a6fd16d9c318696fcf167689baa3` and the full history behind it is present.
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
