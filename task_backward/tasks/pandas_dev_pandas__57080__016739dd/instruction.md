# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Inconsistent resolution from constructing with and assigning datetime values

### Pandas version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [ ] I have confirmed this bug exists on the [main branch](https://pandas.pydata.org/docs/dev/getting_started/install.html#installing-the-development-version-of-pandas) of pandas.


### Reproducible Example

```python
from datetime import datetime
import pandas as pd

construct = pd.DataFrame([datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)])
print(construct.info())

assign = pd.DataFrame([], index=[0])
assign["time"] = datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
print(assign.info())

assign_timestamp = pd.DataFrame([], index=[0])
assign_timestamp["time"] = pd.Timestamp(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
print(assign_timestamp.info())

assign_loc = pd.DataFrame([], index=[0])
assign_loc.loc[0, "time"] = datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
print(assign_loc.info())
```


### Issue Description

Hi! I'm faced with a problem about datetime columns. It was met in our prod env upgrade from pandas 1.5.3 to 2.1.4. Before that constructing and assigning both result in datetime64[ns]. But asof 2.1.4, the following results were get:
```
print(construct.info())
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1 entries, 0 to 0
Data columns (total 1 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   0       1 non-null      datetime64[ns]
dtypes: datetime64[ns](1)
memory usage: 140.0 bytes
None

print(assign.info())
<class 'pandas.core.frame.DataFrame'>
Index: 1 entries, 0 to 0
Data columns (total 1 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   time    1 non-null      datetime64[us]
dtypes: datetime64[us](1)
memory usage: 16.0 bytes
None

print(assign_timestamp.info())
<class 'pandas.core.frame.DataFrame'>
Index: 1 entries, 0 to 0
Data columns (total 1 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   time    1 non-null      datetime64[us]
dtypes: datetime64[us](1)
memory usage: 16.0 bytes
None

print(assign_loc.info())
<class 'pandas.core.frame.DataFrame'>
Index: 1 entries, 0 to 0
Data columns (total 1 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   time    1 non-null      datetime64[ns]
dtypes: datetime64[ns](1)
memory usage: 124.0 bytes
None
```
While construction and loc assignment gives the dtype datetime64[ns], df["time"] = datetime(...) results in datetime64[us].

I tested in a different env using pandas 2.2.0. The result is different when using loc:
```
print(assign_loc.info())
<class 'pandas.core.frame.DataFrame'>
Index: 1 entries, 0 to 0
Data columns (total 1 columns):
 #   Column  Non-Null Count  Dtype         
---  ------  --------------  -----         
 0   time    1 non-null      datetime64[us]
dtypes: datetime64[us](1)
memory usage: 124.0 bytes
None
```

This time assign_loc gives datetime64[us], but construct still gives datetime64[ns].

I've noticed in the release notes that changes were made to `astype`, making it parse inputs according to the original resolution, but it might not explain the inconsistency intuitively. This is causing massive concat errors in our code due to inconsistent dtypes, and we are truly concerned about it as we are not sure if this is a bug and what behavior will be stabilized. We feel like further confirming it.

Thank you so much and wish you all the best!

### Expected Behavior

Consistent datetime resolution

### Installed Versions

<details>
2.1.4

INSTALLED VERSIONS
------------------

python              : 3.11.7.final.0
python-bits         : 64
OS                  : Windows
OS-release          : 10
Version             : 10.0.22621
machine             : AMD64
processor           : Intel64 Family 6 Model 151 Stepping 2, GenuineIntel
byteorder           : little
LC_ALL              : None
LANG                : None
LOCALE              : en_US.UTF-8
pandas              : 2.1.4
numpy               : 1.26.3
pytz                : 2023.3.post1
dateutil            : 2.8.2
setuptools          : 68.2.2
pip                 : 23.3.1
Cython              : None
pytest              : 7.4.0
hypothesis          : None
sphinx              : None
blosc               : None
feather             : None
xlsxwriter          : None
lxml.etree          : 4.9.3
html5lib            : None
pymysql             : 1.0.2
psycopg2            : None
jinja2              : 3.1.2
IPython             : 8.20.0
pandas_datareader   : None
bs4                 : 4.12.2
bottleneck          : 1.3.5
dataframe-api-compat: None
fastparquet         : 2023.8.0
fsspec              : 2023.10.0
gcsfs               : None
matplotlib          : 3.8.0
numba               : 0.58.1
numexpr             : 2.8.7
odfpy               : None
openpyxl            : 3.0.10
pandas_gbq          : None
pyarrow             : 11.0.0
pyreadstat          : None
pyxlsb              : None
s3fs                : None
scipy               : 1.11.4
sqlalchemy          : 2.0.25
tables              : None
tabulate            : None
xarray              : None
xlrd                : None
zstandard           : None
tzdata              : 2023.3
qtpy                : None
pyqt5               : None


TEST 2.2.0：

INSTALLED VERSIONS
------------------

python                : 3.12.0.final.0
python-bits           : 64
OS                    : Windows
OS-release            : 11
Version               : 10.0.22621
machine               : AMD64
processor             : Intel64 Family 6 Model 151 Stepping 2, GenuineIntel
byteorder             : little
LC_ALL                : None
LANG                  : None
LOCALE                : en_US.UTF-8
pandas                : 2.2.0
numpy                 : 1.26.3
pytz                  : 2023.3.post1
dateutil              : 2.8.2
setuptools            : 68.2.2
pip                   : 23.3.2
Cython                : None
pytest                : None
hypothesis            : None
sphinx                : None
blosc                 : None
feather               : None
xlsxwriter            : None
lxml.etree            : None
html5lib              : None
pymysql               : None
psycopg2              : None
jinja2                : 3.1.2
IPython               : 8.18.1
pandas_datareader     : None
adbc-driver-postgresql: None
adbc-driver-sqlite    : None
bs4                   : 4.12.2
bottleneck            : None
dataframe-api-compat  : None
fastparquet           : None
fsspec                : None
gcsfs                 : None
matplotlib            : 3.8.2
numba                 : None
numexpr               : None
odfpy                 : None
openpyxl              : None
pandas_gbq            : None
pyarrow               : None
pyreadstat            : None
python-calamine       : None
pyxlsb                : None
s3fs                  : None
scipy                 : 1.11.4
sqlalchemy            : None
tables                : None
tabulate              : None
xarray                : None
xlrd                  : None
zstandard             : None
tzdata                : 2023.3
qtpy                  : None
pyqt5                 : None


</details>


Bisected this issue, regression happened on this commit:


File used for bisecting
```python
# t.py file

from datetime import datetime
import pandas as pd

construct = pd.DataFrame([datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)])
assert str(construct.iloc[:,0].dtype) == 'datetime64[ns]'

assign = pd.DataFrame([], index=[0])
assign["time"] = datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
assert str(assign.iloc[:,0].dtype) == 'datetime64[ns]'

assign_timestamp = pd.DataFrame([], index=[0])
assign_timestamp["time"] = pd.Timestamp(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
assert str(assign_timestamp.iloc[:,0].dtype) == 'datetime64[ns]'

assign_loc = pd.DataFrame([], index=[0])
assign_loc.loc[0, "time"] = datetime(year=2024, month=1, day=26, hour=0, minute=0, second=0, microsecond=0)
assert str(assign_loc.iloc[:,0].dtype) == 'datetime64[ns]'
```
Before that all dtypes are `datetime64[ns]`
After:
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `d928a5cc222be5968b2f1f8a5f8d02977a8d6c2d` and the full history behind it is present.
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
