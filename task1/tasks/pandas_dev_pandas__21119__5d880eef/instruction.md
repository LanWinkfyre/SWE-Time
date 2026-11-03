# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
pandas 0.23 fails on column<->index boolean merge

#### Code Sample, a copy-pastable example if possible

```python
import pandas as pd

df1 = pd.DataFrame({'x': pd.Series([True, False], dtype=bool)})
df2 = df1.set_index('x')

df1.merge(df2, left_on='x', right_index=True)
```

#### Problem description
On Pandas `0.23`, I get the following Exception:

```
venv/local/lib/python2.7/site-packages/pandas/core/frame.pyc in merge(self, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate)
   6377                      right_on=right_on, left_index=left_index,
   6378                      right_index=right_index, sort=sort, suffixes=suffixes,
-> 6379                      copy=copy, indicator=indicator, validate=validate)
   6380
   6381     def round(self, decimals=0, *args, **kwargs):

venv/local/lib/python2.7/site-packages/pandas/core/reshape/merge.pyc in merge(left, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate)
     58                          right_index=right_index, sort=sort, suffixes=suffixes,
     59                          copy=copy, indicator=indicator,
---> 60                          validate=validate)
     61     return op.get_result()
     62

venv/local/lib/python2.7/site-packages/pandas/core/reshape/merge.pyc in __init__(self, left, right, how, on, left_on, right_on, axis, left_index, right_index, sort, suffixes, copy, indicator, validate)
    552         # validate the merge keys dtypes. We may need to coerce
    553         # to avoid incompat dtypes
--> 554         self._maybe_coerce_merge_keys()
    555
    556         # If argument passed to validate,

venv/local/lib/python2.7/site-packages/pandas/core/reshape/merge.pyc in _maybe_coerce_merge_keys(self)
    976             # incompatible dtypes GH 9780, GH 15800
    977             elif is_numeric_dtype(lk) and not is_numeric_dtype(rk):
--> 978                 raise ValueError(msg)
    979             elif not is_numeric_dtype(lk) and is_numeric_dtype(rk):
    980                 raise ValueError(msg)

ValueError: You are trying to merge on bool and object columns. If you wish to proceed you should use pd.concat
```

#### Expected Output

```
       x
0   True
1  False
```

#### Output of ``pd.show_versions()``

<details>

```
INSTALLED VERSIONS
------------------
commit: None
python: 2.7.13.final.0
python-bits: 64
OS: Linux
OS-release: 4.9.49-moby
machine: x86_64
processor:
byteorder: little
LC_ALL: en_US.UTF-8
LANG: en_US.UTF-8
LOCALE: None.None

pandas: 0.23.0
pytest: 3.4.0
pip: 9.0.3
setuptools: 39.0.1
Cython: 0.28.1
numpy: 1.14.0
scipy: 1.0.0
pyarrow: None
xarray: None
IPython: 5.5.0
sphinx: 1.6.5
patsy: 0.4.1
dateutil: 2.6.1
pytz: 2017.3
blosc: None
bottleneck: 1.2.1
tables: None
numexpr: 2.6.4
feather: None
matplotlib: 2.1.0
openpyxl: None
xlrd: None
xlwt: None
xlsxwriter: None
lxml: None
bs4: None
html5lib: None
sqlalchemy: None
pymysql: None
psycopg2: None
jinja2: 2.8.1
s3fs: None
fastparquet: None
pandas_gbq: None
pandas_datareader: None
```
</details>
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `e033c0616158d3ba974456b4f84810492936b1fe` and the full history behind it is present.
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
