# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: IndexError on read_csv/read_table when using usecols/names parameters and omitting last column

Example code:

``` python
from StringIO import StringIO
import pandas as pd

names = ["a","b","c"]

data = """\
0,1,2
3,4,5
6,7,8"""

# usecols works as expected if all columns are named
print pd.read_csv(StringIO(data), header=None, usecols=[1,2], names=names)
print pd.read_csv(StringIO(data), header=None, usecols=[0,1], names=names)

# naming only columns selected with usecols works when last column is included
print pd.read_csv(StringIO(data), header=None, usecols=[1,2], names=names[1:])
# causes IndexError
print pd.read_csv(StringIO(data), header=None, usecols=[0,1], names=names[:-1])
```

Output:

```
   b  c
0  1  2
1  4  5
2  7  8

[3 rows x 2 columns]
   a  b
0  0  1
1  3  4
2  6  7

[3 rows x 2 columns]
   b  c
0  1  2
1  4  5
2  7  8

[3 rows x 2 columns]
Traceback (most recent call last):
  File "pandas_test2.py", line 18, in <module>
    print pd.read_csv(StringIO(data), header=None, usecols=[0,1], names=names[:-1])
  File "/home/weston/pandas/pandas/io/parsers.py", line 404, in parser_f
    return _read(filepath_or_buffer, kwds)
  File "/home/weston/pandas/pandas/io/parsers.py", line 212, in _read
    return parser.read()
  File "/home/weston/pandas/pandas/io/parsers.py", line 610, in read
    ret = self._engine.read(nrows)
  File "/home/weston/pandas/pandas/io/parsers.py", line 1050, in read
    data = self._reader.read(nrows)
  File "parser.pyx", line 727, in pandas.parser.TextReader.read (pandas/parser.c:6475)
  File "parser.pyx", line 749, in pandas.parser.TextReader._read_low_memory (pandas/parser.c:6695)
  File "parser.pyx", line 824, in pandas.parser.TextReader._read_rows (pandas/parser.c:7517)
  File "parser.pyx", line 902, in pandas.parser.TextReader._convert_column_data (pandas/parser.c:8296)
  File "parser.pyx", line 1139, in pandas.parser.TextReader._get_column_name (pandas/parser.c:11353)
IndexError: list index out of range
```

`print_versions.py` output:




I can repro. 

Looking into it.
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `2485e0934e90c2f3bd16967c3d36b0cd3b8413bf` and the full history behind it is present.
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
