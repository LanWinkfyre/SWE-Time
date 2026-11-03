# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: read_csv call with skiprows fails on pandas versions 0.15.2, 0.16.0, works on 0.15.0 and 0.15.1

```
# passes for 0.15.0
# passes for 0.15.1
# fails for 0.15.2
# fails for 0.16.0
# This is for a "csv" file where there are a number of initial rows to be skipped at file start.
import pandas as pd
import urllib

test_data_url = 'http://www.bom.gov.au/fwo/IDV60901/IDV60901.95936.axf'
test_file = 'test.csv'

ROWS_TO_SKIP_AT_THE_START = 19


def main():
    urllib.urlretrieve(test_data_url, test_file)
    print('pandas version: {}'.format(pd.version.version))
    data = pd.read_csv(test_file, skiprows=ROWS_TO_SKIP_AT_THE_START)
    assert len(data) == 145
    assert 'sort_order' in data
    print('file successfully read by read_csv()')



if __name__ == '__main__':
    main()
```
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `702be31ec71b2fe4ec40b72b9bc06804fd1a7373` and the full history behind it is present.
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
