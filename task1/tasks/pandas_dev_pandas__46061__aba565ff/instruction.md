# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: groupby().rolling("freq") validation raises even if dates are sorted within each group

### Pandas version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [X] I have confirmed this bug exists on the main branch of pandas.


### Reproducible Example

```python
import pandas as pd
print(pd.__version__)
test_df = pd.DataFrame({
    'Name':['L', 'L', 'L',
                    'M', 'M', 'M', 'M', 'M', 'M'],
    'ID': ['L1', 'L2', 'L3',
              'M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
    'Date': [
        '2005-01-01', '2006-01-01', '2013-01-01', 
        '2005-01-01', '2006-01-01', '2006-01-01', '2017-01-01', '2006-02-01', '2006-03-01'],
    'indicator': [0, 1, 0,
                          0, 1, 0, 0, 1, 0],
    'rolling_sum':[0, 0, 1,
                              0, 0, 0, 0, 1, 2]})
test_df['Date'] = pd.to_datetime(test_df['Date'], errors='coerce')
test_df.groupby('Name').rolling('731D', on='Date')['indicator'].sum().reset_index()
```


### Issue Description

Grouping by a column and then rolling over the grouped dataframe results in `[ValueError: Date must be monotonic]()`. Ultimately, the operation should be able to produce the `rolling_sum` column in the example.

### Expected Behavior

This is not an issue in pandas `1.3.5` but is an issue in `1.4` and higher. I expect this function to create a grouped dataframe and to then perform the rolling summation on the provided column using the date window provided. 

### Installed Versions

<details>


INSTALLED VERSIONS
------------------

python           : 3.8.12.final.0
python-bits      : 64
OS               : Darwin
OS-release       : 21.1.0
Version          : Darwin Kernel Version 21.1.0: Wed Oct 13 17:33:24 PDT 2021; root:xnu-8019.41.5~1/RELEASE_ARM64_T8101
machine          : x86_64
processor        : i386
byteorder        : little
LC_ALL           : None
LANG             : None
LOCALE           : None.UTF-8

pandas           : 1.4.1
numpy            : 1.22.2
pytz             : 2021.3
dateutil         : 2.8.2
pip              : 22.0.3
setuptools       : 60.6.0
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
jinja2           : 3.0.3
IPython          : 8.0.1
pandas_datareader: None
bs4              : None
bottleneck       : None
fastparquet      : None
fsspec           : None
gcsfs            : None
matplotlib       : None
numba            : None
numexpr          : None
odfpy            : None
openpyxl         : 3.0.9
pandas_gbq       : None
pyarrow          : 6.0.1
pyreadstat       : None
pyxlsb           : None
s3fs             : None
scipy            : None
sqlalchemy       : None
tables           : None
tabulate         : None
xarray           : None
xlrd             : None
xlwt             : None
zstandard        : None


</details>


> But even if the dates are sorted with the groups this error still raised which seems like a bug

since this worked (for the sorted groups case) in 1.3.5, labelling as a regression.
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `1bd193eebad6897989bbf06ae62adcffefdf97cd` and the full history behind it is present.
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
