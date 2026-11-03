# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Unary minus raises for series with Int64Dtype

- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.



---


#### Code Sample, a copy-pastable example

```python
>>> import pandas as pd
>>> pd.__version__
'1.1.1'
>>> s = pd.Series([1, 2, 3], dtype="Int64")
>>> -s
Traceback (most recent call last):
  File "...", line 1, in <module>
    -s
  File ".../lib/python3.8/site-packages/pandas/core/generic.py", line 1297, in __neg__
    arr = operator.neg(values)
TypeError: bad operand type for unary -: 'IntegerArray'
```


#### Problem description

I cannot negate series with Int64Dtype. This was possible in previous versions (but it returned object dtype).

#### Expected Output

```
>>> import pandas as pd
>>> pd.__version__
'1.0.5'
>>> s = pd.Series([1, 2, 3], dtype="Int64")
>>> -s
0    -1
1    -2
2    -3
dtype: object
```

#### Output of ``pd.show_versions()``

<details>


INSTALLED VERSIONS
------------------

python           : 3.8.3.final.0
python-bits      : 64
OS               : Darwin
OS-release       : 19.6.0
Version          : Darwin Kernel Version 19.6.0: Thu Jun 18 20:49:00 PDT 2020; root:xnu-6153.141.1~1/RELEASE_X86_64
machine          : x86_64
processor        : i386
byteorder        : little
LC_ALL           : None
LANG             : en_US.UTF-8
LOCALE           : en_US.UTF-8

pandas           : 1.1.1
numpy            : 1.19.1
pytz             : 2020.1
dateutil         : 2.8.1
pip              : 20.1.1
setuptools       : 47.3.1
Cython           : None
pytest           : None
hypothesis       : None
sphinx           : None
blosc            : None
feather          : None
xlsxwriter       : None
lxml.etree       : None
html5lib         : None
pymysql          : None
psycopg2         : None
jinja2           : None
IPython          : 7.15.0
pandas_datareader: None
bs4              : None
bottleneck       : None
fsspec           : None
fastparquet      : None
gcsfs            : None
matplotlib       : None
numexpr          : None
odfpy            : None
openpyxl         : None
pandas_gbq       : None
pyarrow          : None
pytables         : None
pyxlsb           : None
s3fs             : None
scipy            : None
sqlalchemy       : None
tables           : None
tabulate         : None
xarray           : None
xlrd             : None
xlwt             : None
numba            : None

</details>


 

bisect log
<details>


</details>

setup to reproduce
<details>

Ran bisection with this shell script, first good/bad commits are 1.0.5 and 1.1.0 releases respectively:
```
set -eu
python3 setup.py build_ext --inplace --force
python3 un.py
```

where un.py is

```python
import pandas

s = pandas.Series([1, 2, 3], dtype="Int64")

print(-s)
```
</details>
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `73c1d3269830d787c8990de8f02bf4279d2720ab` and the full history behind it is present.
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
