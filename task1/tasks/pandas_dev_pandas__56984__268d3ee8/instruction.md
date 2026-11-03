# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Unsafe decimal parse for arrow types silently truncates value instead of raising an error

### Pandas version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [X] I have confirmed this bug exists on the [main branch](https://pandas.pydata.org/docs/dev/getting_started/install.html#installing-the-development-version-of-pandas) of pandas.


### Reproducible Example

```python
>>> ser = pd.Series(["1.2345"], dtype=pd.ArrowDtype(pa.string()))
>>> ser.astype(pd.ArrowDtype(pa.decimal128(1, 0)))
0    1
dtype: decimal128(1, 0)[pyarrow]
>>>
```


### Issue Description

The value is silently truncated, instead of raising an error that the decimal cannot be safely rescaled. This example would raise this error in pandas 2.1.4:

```
>>> ser = pd.Series(["1.2345"], dtype=pd.ArrowDtype(pa.string()))
>>> ser.astype(pd.ArrowDtype(pa.decimal128(1, 0)))
pyarrow.lib.ArrowInvalid: Rescaling Decimal128 value would cause data loss
>>> pd.__version__
'2.1.4'
>>>
```

For decimal most usages values accuracy, and silently truncating the value does not seem desirable, also if the original series was a decimal, then this error would be raised:

```
>>> ser = pd.Series(["1.2345"], dtype=pd.ArrowDtype(pa.decimal128(5, 4)))
>>> ser.astype(pd.ArrowDtype(pa.decimal128(1,0)))
pyarrow.lib.ArrowInvalid: Rescaling Decimal128 value would cause data loss
>>>
```

So it seems unusual when casting a decimal from a string, the value is silently truncated during rescale, but when casting it from another decimal, then there's no truncation during the rescale operation and an error is raised.



### Expected Behavior

```
>>> ser = pd.Series(["1.2345"], dtype=pd.ArrowDtype(pa.string()))
>>> ser.astype(pd.ArrowDtype(pa.decimal128(1, 0)))
pyarrow.lib.ArrowInvalid: Rescaling Decimal128 value would cause data loss
```

This was the behavior in pandas 2.1.4.

### Installed Versions

<details>

INSTALLED VERSIONS
------------------

python                : 3.11.7.final.0
python-bits           : 64
OS                    : Windows
OS-release            : 10
Version               : 10.0.22631
machine               : AMD64
processor             : Intel64 Family 6 Model 151 Stepping 2, GenuineIntel
byteorder             : little
LC_ALL                : None
LANG                  : None
LOCALE                : English_United States.1252

pandas                : 2.2.0
numpy                 : 1.26.2
pytz                  : 2023.3.post1
dateutil              : 2.8.2
setuptools            : 68.2.2
pip                   : 23.3.1
Cython                : None
pytest                : None
hypothesis            : None
sphinx                : 4.2.0
blosc                 : None
feather               : None
xlsxwriter            : None
lxml.etree            : None
html5lib              : None
pymysql               : None
psycopg2              : None
jinja2                : 3.1.2
IPython               : 8.17.2
pandas_datareader     : None
adbc-driver-postgresql: None
adbc-driver-sqlite    : None
bs4                   : 4.12.2
bottleneck            : None
dataframe-api-compat  : None
fastparquet           : None
fsspec                : None
gcsfs                 : None
matplotlib            : None
numba                 : None
numexpr               : None
odfpy                 : None
openpyxl              : None
pandas_gbq            : None
pyarrow               : 14.0.0
pyreadstat            : None
python-calamine       : None
pyxlsb                : None
s3fs                  : None
scipy                 : None
sqlalchemy            : None
tables                : None
tabulate              : 0.9.0
xarray                : None
xlrd                  : None
zstandard             : None
tzdata                : 2023.3
qtpy                  : None
pyqt5                 : None
>>>

</details>





cc @mroeschke
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `5849cc7c3bfded6a1ebc3ad46f621268ed8d97cf` and the full history behind it is present.
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
