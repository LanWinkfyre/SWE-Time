# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ImportError: No module named sparse.api

Pulled from github master and did install (removed previous version and build dir), but get ImportError.

``` python
In [1]: import pandas
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
...
----> 1 import pandas

<...>/lib/python2.7/site-packages/pandas/__init__.py in <module>()
     21
     22 from pandas.core.api import *
---> 23 from pandas.sparse.api import *
     24 from pandas.stats.api import *
     25

ImportError: No module named sparse.api

In [2]:
```

There is no sparce directory in <...>/lib/python2.7/site-packages/pandas.
If i build in place and import from the src directory there is no ImportError.

UPDATE:
Running git bisect, gives the following commits as first _bad_ commit;
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `cc463925b7b5991ec3e900c1c68f09e66dcc31a8` and the full history behind it is present.
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
