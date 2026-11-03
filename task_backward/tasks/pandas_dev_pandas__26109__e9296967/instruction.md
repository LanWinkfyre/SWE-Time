# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Constructing PeriodIndex with string data

#### Code Sample, a copy-pastable example if possible

```python
# quarters as string representation
quarters = pd.Series(["2018Q1", "2018Q2", "2018Q1", "2018Q3"])

# gives TypeError (see details for stack trace)
pi = pd.PeriodIndex(quarters, freq="Q")
TypeError: Incorrect dtype

# works as intended
pi = pd.PeriodIndex(quarters.values, freq="Q")
```
#### Problem description
Creating a PeriodIndex with string data fails when using a pandas.Series but works if using the underlying np.array.

Is this expected behavior?
#### Output of stack trace
<details>

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-6-1d88474891ea> in <module>
----> 1 pi = pd.PeriodIndex(quarters, freq="Q")

/usr/local/anaconda3/envs/PCS/lib/python3.7/site-packages/pandas/core/indexes/period.py in __new__(cls, data, ordinal, freq, start, end, periods, tz, dtype, copy, name, **fields)
    238             else:
    239                 # don't pass copy here, since we copy later.
--> 240                 data = period_array(data=data, freq=freq)
    241 
    242         if copy:

/usr/local/anaconda3/envs/PCS/lib/python3.7/site-packages/pandas/core/arrays/period.py in period_array(data, freq, copy)
    767         return PeriodArray._from_datetime64(data, freq)
    768     if isinstance(data, (ABCPeriodIndex, ABCSeries, PeriodArray)):
--> 769         return PeriodArray(data, freq)
    770 
    771     # other iterable of some kind

/usr/local/anaconda3/envs/PCS/lib/python3.7/site-packages/pandas/core/arrays/period.py in __init__(self, values, freq, dtype, copy)
    155             values = values._values
    156             if not isinstance(values, type(self)):
--> 157                 raise TypeError("Incorrect dtype")
    158 
    159         elif isinstance(values, ABCPeriodIndex):

TypeError: Incorrect dtype

```
</details>


#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit: None
python: 3.7.2.final.0
python-bits: 64
OS: Darwin
OS-release: 18.2.0
machine: x86_64
processor: i386
byteorder: little
LC_ALL: en_US.UTF-8
LANG: en_US.UTF-8
LOCALE: en_US.UTF-8

pandas: 0.24.1
pytest: None
pip: 19.0.3
setuptools: 40.8.0
Cython: 0.29.5
numpy: 1.15.4
scipy: 1.2.1
pyarrow: 0.11.1
xarray: None
IPython: 7.3.0
sphinx: None
patsy: None
dateutil: 2.8.0
pytz: 2018.9
blosc: None
bottleneck: None
tables: None
numexpr: None
feather: None
matplotlib: 3.0.3
openpyxl: 2.6.1
xlrd: 1.2.0
xlwt: None
xlsxwriter: None
lxml.etree: None
bs4: None
html5lib: None
sqlalchemy: None
pymysql: None
psycopg2: None
jinja2: 2.10
s3fs: None
fastparquet: None
pandas_gbq: None
pandas_datareader: None
gcsfs: None

</details>


> That's certainly not expected behaviour, and it is actually also a regression compared to 0.23.4.

 24.0)
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `fd1c3f868d2d8f8763cf126054ebbb5ae367017a` and the full history behind it is present.
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
