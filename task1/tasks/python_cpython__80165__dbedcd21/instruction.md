# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test__xxsubinterpreters leaked [3, 4, 3] memory blocks, sum=1

BPO | [35984](https://bugs.python.org/issue35984)
--- | :---
Nosy | @vstinner, @ericsnowcurrently, @izbyshev, @pablogsal, @miss-islington
PRs | <li>python/cpython#11845</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = 'https://github.com/izbyshev'
closed_at = <Date 2019-02-15.22:35:12.462>
created_at = <Date 2019-02-13.11:10:03.433>
labels = ['3.8', 'tests', 'performance']
title = 'test__xxsubinterpreters leaked [3, 4, 3] memory blocks, sum=1'
updated_at = <Date 2019-02-15.22:35:12.462>
user = 'https://github.com/pablogsal'
```

bugs.python.org fields:
```python
activity = <Date 2019-02-15.22:35:12.462>
actor = 'eric.snow'
assignee = 'izbyshev'
closed = True
closed_date = <Date 2019-02-15.22:35:12.462>
closer = 'eric.snow'
components = ['Tests']
creation = <Date 2019-02-13.11:10:03.433>
creator = 'pablogsal'
dependencies = []
files = []
hgrepos = []
issue_num = 35984
keywords = ['patch']
message_count = 11.0
messages = ['335408', '335409', '335411', '335412', '335414', '335421', '335461', '335462', '335477', '335652', '335653']
nosy_count = 5.0
nosy_names = ['vstinner', 'eric.snow', 'izbyshev', 'pablogsal', 'miss-islington']
pr_nums = ['11845']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'resource usage'
url = 'https://bugs.python.org/issue35984'
versions = ['Python 3.8']
```

</p></details>


The reafleak buildbots have detected memory block leaks in test__xxsubinterpreters:

Ran 112 tests in 4.721s
OK (skipped=5)
.
test__xxsubinterpreters leaked [3, 4, 3] memory blocks, sum=10
1 test failed again:
    test__xxsubinterpreters
== Tests result: FAILURE then FAILURE ==


https://buildbot.python.org/all/#/builders/1/builds/502
https://buildbot.python.org/all/#/builders/80/builds/511
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `cfd31f0af20f76849bbec6185efea01c72349f2a` and the full history behind it is present.
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
