# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Index.str.partition gives ValueError while trying to compute index name (expand=False)


#### Code Sample, a copy-pastable example if possible

```
python3 -c 'import pandas; pandas.Index(["a,b", "c,d"], name="hello").str.partition(",")'
```

``` pytb
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/pwaller/.local/src/pandas/pandas/core/strings.py", line 1432, in partition
    return self._wrap_result(result, expand=expand)
  File "/home/pwaller/.local/src/pandas/pandas/core/strings.py", line 1348, in _wrap_result
    return MultiIndex.from_tuples(result, names=name)
  File "/home/pwaller/.local/src/pandas/pandas/indexes/multi.py", line 889, in from_tuples
    return MultiIndex.from_arrays(arrays, sortorder=sortorder, names=names)
  File "/home/pwaller/.local/src/pandas/pandas/indexes/multi.py", line 844, in from_arrays
    names=names, verify_integrity=False)
  File "/home/pwaller/.local/src/pandas/pandas/indexes/multi.py", line 92, in __new__
    result._set_names(names)
  File "/home/pwaller/.local/src/pandas/pandas/indexes/multi.py", line 446, in _set_names
    raise ValueError('Length of names must match number of levels in '
ValueError: Length of names must match number of levels in MultiIndex.
```
#### Expected Output

``` python
In [1]: import pandas; pandas.Index(["a,b", "c,d"], name="hello").str.partition(",")
Out[1]: 
MultiIndex(levels=[['a', 'c'], [','], ['b', 'd']],
           labels=[[0, 1], [0, 0], [0, 1]])
```
#### Versions

 The problem is not present in 0.17.1 and is present in 0.18.0rc2. 

Note: when I use a `name="foo"`, it happens to work because it has the correct length, the index name ends up being `["f", "o", "o"]`, so it's possible this is tested somewhere and happens to work even though it's not correct for a large number of use cases.
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `ed3d1453f354a68999a4517f0e6641b11f2a9b9a` and the full history behind it is present.
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
