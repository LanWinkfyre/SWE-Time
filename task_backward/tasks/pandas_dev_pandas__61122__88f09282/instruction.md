# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: ``Series.interpolate`` regression in latest Pandas 3.0.0 nightly (method 'linear' behaves like 'index')

### Pandas version checks

- [x] I have checked that this issue has not already been reported.

- [ ] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [x] I have confirmed this bug exists on the [main branch](https://pandas.pydata.org/docs/dev/getting_started/install.html#installing-the-development-version-of-pandas) of pandas.


### Reproducible Example

```python
import numpy as np
import pandas as pd

s = pd.Series([1.0, np.nan, 3.0], index=[1, 3, 4])
s.interpolate(method='linear')
s.interpolate(method='index')
```

### Issue Description

The interpolation method 'linear' behaves like the method 'index' with current Pandas 3.0.0 nightly. This is a regression from 2.2.3.

According to the documentation (stable and dev):

> Interpolation technique to use. One of:
>
>  - ‘linear’: Ignore the index and treat the values as equally spaced. This is the only method supported on MultiIndexes.
> [...]
>  - ‘index’: The interpolation uses the numerical values of the DataFrame’s index to linearly calculate missing values.

In the example above, the index is not linearly spaced. But both interpolation methods return the output that is expected for the 'index' method when using the latest Pandas 3.0.0 nightly.

```
>>> s.interpolate(method='linear')
1    1.000000
3    2.333333
4    3.000000
dtype: float64
>>> s.interpolate(method='index')
1    1.000000
3    2.333333
4    3.000000
dtype: float64
```

### Expected Behavior

The output should be different and ``'linear'`` should ignore the non-linearly spaced index. The expected output should be the same as with Pandas 2.2.3:

```
>>> s.interpolate(method='linear')
1    1.0
3    2.0
4    3.0
dtype: float64
>>> s.interpolate(method='index')
1    1.000000
3    2.333333
4    3.000000
dtype: float64
```

### Installed Versions

<details>

INSTALLED VERSIONS
------------------

python                : 3.12.1
python-bits           : 64
OS                    : Windows
OS-release            : 10
Version               : 10.0.19044
machine               : AMD64
processor             : AMD64 Family 23 Model 113 Stepping 0, AuthenticAMD
byteorder             : little
LC_ALL                : None
LANG                  : None
LOCALE                : English_United Kingdom.1252


numpy                 : 2.3.0.dev0+git20250311.a651643
dateutil              : 2.9.0.post0
pip                   : 23.2.1
Cython                : None
sphinx                : None
IPython               : None
adbc-driver-postgresql: None
adbc-driver-sqlite    : None
bs4                   : None
blosc                 : None
bottleneck            : None
fastparquet           : None
fsspec                : None
html5lib              : None
hypothesis            : None
gcsfs                 : None
jinja2                : None
lxml.etree            : None
matplotlib            : None
numba                 : None
numexpr               : None
odfpy                 : None
openpyxl              : None
psycopg2              : None
pymysql               : None
pyarrow               : None
pyreadstat            : None
pytest                : None
python-calamine       : None
pytz                  : None
pyxlsb                : None
s3fs                  : None
scipy                 : None
sqlalchemy            : None
tables                : None
tabulate              : None
xarray                : None
xlrd                  : None
xlsxwriter            : None
zstandard             : None
tzdata                : 2025.1
qtpy                  : None
pyqt5                 : None

</details>


Thanks for the report! A git-bisect reveals:





cc @cbpygit @mroeschke @MarcoGorelli
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `8943c97c597677ae989d47e612705f088aab4cd0` and the full history behind it is present.
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
