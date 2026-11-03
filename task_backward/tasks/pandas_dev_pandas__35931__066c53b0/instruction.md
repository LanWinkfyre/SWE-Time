# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: breaking change in df.replace() from 1.0.5 to 1.1.0

- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.

- [x] (optional) I have confirmed this bug exists on the master branch of pandas.

---

**Note**: Please read [this guide](https://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports) detailing how to provide the necessary information for us to reproduce your bug.

#### Code Sample, a copy-pastable example

```python
# Your code here
df = pd.DataFrame({"age": range(1,100)})
df["age"] = pd.cut(df["age"], [0, 50, 65, 99], right=False)
df.replace(to_replace={
    "age":{
        pd.Interval(0, 50, closed='left'): "Ages < 50",
        pd.Interval(50, 65, closed='left'): "Ages 50-64",
        pd.Interval(65, 99, closed='left'): "Ages 65+"
    }
})
```

#### Problem description

The above sample code works in 1.0.5 but error out in 1.1.0 and above with error msg:
```
TypeError: Cannot compare types 'ndarray(dtype=object)' and 'Interval'
```
It only happens with pd.Interval dtype, nested dict of string to string mapping works fine. 

#### Expected Output

#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------

python           : 3.7.6.final.0
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


numpy            : 1.19.1
pytz             : 2020.1
dateutil         : 2.8.1
pip              : 20.2.2
setuptools       : 49.6.0.post20200814
Cython           : 0.29.21
pytest           : 6.0.1
hypothesis       : 5.29.0
sphinx           : 2.4.0
blosc            : None
feather          : None
xlsxwriter       : 1.3.3
lxml.etree       : 4.5.2
html5lib         : 1.1
pymysql          : None
psycopg2         : 2.8.4 (dt dec pq3 ext lo64)
jinja2           : 2.11.2
IPython          : 7.17.0
pandas_datareader: None
bs4              : 4.9.1
bottleneck       : 1.3.2
fsspec           : 0.8.0
fastparquet      : 0.4.1
gcsfs            : None
matplotlib       : 3.3.1
numexpr          : 2.7.1
odfpy            : None
openpyxl         : 3.0.5
pandas_gbq       : None
pyarrow          : 0.15.1
pytables         : None
pyxlsb           : None
s3fs             : 0.2.0
scipy            : 1.5.2
sqlalchemy       : 1.3.19
tables           : 3.6.1
tabulate         : 0.8.7
xarray           : 0.16.0
xlrd             : 1.2.0
xlwt             : 1.3.0
numba            : 0.50.1

</details>
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `e3bcf8d1949833793ff50cca393240dab0f0d461` and the full history behind it is present.
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
