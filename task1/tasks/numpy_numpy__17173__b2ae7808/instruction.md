# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression in array creation `np.array([...], dtype='(2,2)f4')` RuntimeError  (Zarr testsuite )

<!-- Please describe the issue in detail here, and fill in the fields below -->

### Reproducing code example:

This is used as a test case in the Zarr codebase

```
import numpy as np
a = np.array([((0, 1),
                       (1, 2)),
                      ((1, 2),
                       (2, 3)),
                      ((2, 3),
                       (3, 4))], dtype='(2,2)f4')
```
### Error message:

```python
In [1]: import numpy as np
   ...: a = np.array([((0, 1),
   ...:                        (1, 2)),
   ...:                       ((1, 2),
   ...:                        (2, 3)),
   ...:                       ((2, 3),
   ...:                        (3, 4))], dtype='(2,2)f4')
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-1-0a6ed20baa50> in <module>
      5                        (2, 3)),
      6                       ((2, 3),
----> 7                        (3, 4))], dtype='(2,2)f4')

RuntimeError: Inconsistent object during array creation? Content of sequences changed (now too shallow).
```

### Numpy/Python version information:



Multiple Pythons (3.7, 3.8), Multiple OS (Mac, Linux), though I bisected only on Linux/3.7.

I
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `5bf6d68e7241498556ee1b28fc146c1c21fbb5e4` and the full history behind it is present.
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
