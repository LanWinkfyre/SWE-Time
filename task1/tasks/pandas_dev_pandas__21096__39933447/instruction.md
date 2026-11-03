# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
regression in 0.23.0 on rolling max with DatetimeIndex.

Behaviour of .rolling() with datetimeindex appears to have changed or regressed between 0.22 & 0.23 versions of pandas.

See below for cut-down test case exhibiting behaviour.

Also see below for different output produced on same code on same data with 2 different pandas versions.

```python
import numpy as np
import pandas as pd


def main():
    print('pandas', pd.__version__)
    n = 10
    index = pd.date_range(
        start='2018-1-1 01:00:00',
        freq='1min',
        periods=n,
    )
    s = pd.Series(
        data=0,
        index=index,
    )
    s.iloc[1] = np.nan
    s.iloc[-1] = 2
    print(s)
    maxes = s.rolling(window=f'{n}min').max()
    print(maxes.value_counts(dropna=False))


if __name__ == '__main__':
    main()
```

ACTUAL OUTPUT
```
pandas 0.22.0      
2018-01-01 01:00:00    0.0             
2018-01-01 01:01:00    NaN             
2018-01-01 01:02:00    0.0             
2018-01-01 01:03:00    0.0             
2018-01-01 01:04:00    0.0             
2018-01-01 01:05:00    0.0             
2018-01-01 01:06:00    0.0             
2018-01-01 01:07:00    0.0             
2018-01-01 01:08:00    0.0             
2018-01-01 01:09:00    2.0             
Freq: T, dtype: float64                
0.0    9           
2.0    1           
dtype: int64       
pandas 0.23.0      
2018-01-01 01:00:00    0.0             
2018-01-01 01:01:00    NaN             
2018-01-01 01:02:00    0.0             
2018-01-01 01:03:00    0.0             
2018-01-01 01:04:00    0.0             
2018-01-01 01:05:00    0.0             
2018-01-01 01:06:00    0.0             
2018-01-01 01:07:00    0.0             
2018-01-01 01:08:00    0.0             
2018-01-01 01:09:00    2.0             
Freq: T, dtype: float64                
0.0    10          
dtype: int64       

```
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `1ee5ecf3ddbf1ce92e1a78e90a4ef07fc3cf0840` and the full history behind it is present.
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
