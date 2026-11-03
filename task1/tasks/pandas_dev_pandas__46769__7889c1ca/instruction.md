# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Pandas Index fails with `bitwise` ufuncs

### Pandas version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [ ] I have confirmed this bug exists on the main branch of pandas.


### Reproducible Example

```python
import pandas as pd
import numpy as np
print(pd.__version__)
print(np.__version__)
pandas_idx = [pd.Int64Index([6, 5, 3, 6, 5, 6, 3, 7, 7, 7, 2, 2, 9, 4, 2, 7, 4, 4, 7, 2, 2, 8,
            3, 9, 9, 5, 4, 2, 4, 8, 9, 3, 7, 4, 6, 1, 3, 6, 7, 7, 6, 4, 2, 4,
            6, 5, 1, 9, 6, 2, 9, 1, 5, 4, 7, 2, 1, 1, 7, 7, 3, 4, 6, 1, 1, 5,
            6, 3, 7, 3, 7, 2, 1, 2, 8, 7, 3, 1, 9, 5, 7, 7, 2, 1, 5, 6, 2, 3,
            4, 2, 2, 6, 2, 4, 8, 2, 8, 2, 2, 2],
           dtype='int64'), pd.Int64Index([5, 6, 3, 1, 8, 3, 7, 2, 8, 8, 7, 5, 5, 3, 5, 2, 8, 5, 6, 2, 1, 7,
            9, 6, 6, 7, 2, 1, 5, 3, 7, 3, 4, 3, 1, 8, 8, 8, 1, 2, 8, 3, 3, 3,
            2, 2, 5, 5, 9, 1, 4, 5, 8, 3, 3, 9, 3, 9, 9, 5, 1, 6, 8, 2, 1, 6,
            5, 7, 9, 4, 8, 6, 5, 8, 8, 7, 2, 6, 4, 1, 4, 7, 2, 4, 4, 7, 2, 3,
            8, 1, 4, 1, 2, 3, 3, 9, 6, 8, 1, 1],
           dtype='int64')]
res = np.bitwise_and(*pandas_idx)
print(res)
print(np.bitwise_and(6, 5))


1.4.2
1.22.3
del3.py:5: FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
  pandas_idx = [pd.Int64Index([6, 5, 3, 6, 5, 6, 3, 7, 7, 7, 2, 2, 9, 4, 2, 7, 4, 4, 7, 2, 2, 8,
del3.py:10: FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
  dtype='int64'), pd.Int64Index([5, 6, 3, 1, 8, 3, 7, 2, 8, 8, 7, 5, 5, 3, 5, 2, 8, 5, 6, 2, 1, 7,
del3.py:16: FutureWarning: Index.__and__ operating as a set operation is deprecated, in the future this will be a logical operation matching Series.__and__.  Use index.intersection(other) instead.
  res = np.bitwise_and(*pandas_idx)
Int64Index([6, 5, 3, 7, 2, 9, 4, 8, 1], dtype='int64')
4
```


### Issue Description

When calling bitwise numpy ufuncs on Index objects, they seem to return wrong results. For instance `numpy.bitwise_and`, `numpy.bitwise_or` and `numpy.bitwise_xor` are the ones that worked correctly until pandas 1.3.5 and returning wrong results afterwards.

### Expected Behavior

```python
1.3.5
1.22.3
Int64Index([4, 4, 3, 0, 0, 2, 3, 2, 0, 0, 2, 0, 1, 0, 0, 2, 0, 4, 6, 2, 0, 0,
            1, 0, 0, 5, 0, 0, 4, 0, 1, 3, 4, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 0,
            2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 1, 1, 1, 5, 1, 4, 0, 0, 1, 4,
            4, 3, 1, 0, 0, 2, 1, 0, 8, 7, 2, 0, 0, 1, 4, 7, 2, 0, 4, 6, 2, 3,
            0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
           dtype='int64')
4
```

### Installed Versions

<details>

Replace this line with the output of pd.show_versions()

</details>


Thanks @galipremsagar for the report.

> For instance `numpy.bitwise_and`, `numpy.bitwise_or` and `numpy.bitwise_xor` are the ones that worked correctly until pandas 1.3.5 and returning wrong results afterwards.



cc @jbrockmendel
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `0d07c2361b13a24afc7cd2bf91e642474f313195` and the full history behind it is present.
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
