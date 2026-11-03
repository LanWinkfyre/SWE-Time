# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Union of two DateTimeIndexes is incorrectly calculated

### Pandas version checks

- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [ ] I have confirmed this bug exists on the [main branch](https://pandas.pydata.org/docs/dev/getting_started/install.html#installing-the-development-version-of-pandas) of pandas.


### Reproducible Example

```python
from pandas import DatetimeIndex

l = DatetimeIndex(['2023-05-24 00:00:00+00:00', '2023-05-24 00:15:00+00:00',
               '2023-05-24 00:30:00+00:00', '2023-05-24 00:45:00+00:00',
               '2023-05-24 01:00:00+00:00'],
              dtype='datetime64[ms, UTC]', name='ts', freq='15min') 

r = DatetimeIndex(['2023-05-24 00:00:00+00:00', '2023-05-24 00:30:00+00:00',
               '2023-05-24 01:00:00+00:00'],
              dtype='datetime64[ms, UTC]', name='ts', freq='30min') 

union = r.union(l)

print(union)

assert len(union) == len(l)
assert all(r.union(l) == l)
```

### Issue Description

The union of two datetime-indexes as given in the reproducible example is calculated incorrectly, the result on newer Pandas versions is

```python
DatetimeIndex(['2023-05-24 00:00:00+00:00', '2051-11-29 16:00:00+00:00',
               '2080-06-06 08:00:00+00:00'],
              dtype='datetime64[ms, UTC]', name='ts', freq='15T')
```

The first failing version is the one I put into "Installed Versions". The error happens exactly from Pandas 2.1.0 onwards, Pandas 1.* and up to 2.0.3 work fine. Neither the numpy nor the Python version matter.

### Expected Behavior

The expected result in the given case is that `l` is returned.

### Installed Versions

INSTALLED VERSIONS
------------------

python              : 3.10.16.final.0
python-bits         : 64
OS                  : Linux
OS-release          : 6.12.10-200.fc41.x86_64
Version             : #1 SMP PREEMPT_DYNAMIC Fri Jan 17 18:05:24 UTC 2025
machine             : x86_64
processor           : 
byteorder           : little
LC_ALL              : None
LANG                : en_US.UTF-8
LOCALE              : en_US.UTF-8

pandas              : 2.1.0
numpy               : 1.26.4
pytz                : 2024.2
dateutil            : 2.9.0.post0
tzdata              : 2025.1
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `c430c613e6c712a39d07146b8adb083d55943840` and the full history behind it is present.
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
