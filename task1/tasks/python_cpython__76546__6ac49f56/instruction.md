# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Reference leak: test_ast test_builtin test_compile

BPO | [32365](https://bugs.python.org/issue32365)
--- | :---
Nosy | @vstinner, @serhiy-storchaka


<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2017-12-18.13:12:47.013>
created_at = <Date 2017-12-18.11:24:03.344>
labels = ['3.7', 'tests', 'performance']
title = 'Reference leak: test_ast test_builtin test_compile'
updated_at = <Date 2017-12-18.13:12:47.012>
user = 'https://github.com/vstinner'
```

bugs.python.org fields:
```python
activity = <Date 2017-12-18.13:12:47.012>
actor = 'serhiy.storchaka'
assignee = 'none'
closed = True
closed_date = <Date 2017-12-18.13:12:47.013>
closer = 'serhiy.storchaka'
components = ['Tests']
creation = <Date 2017-12-18.11:24:03.344>
creator = 'vstinner'
dependencies = []
files = []
hgrepos = []
issue_num = 32365
keywords = ['patch']
message_count = 5.0
messages = ['308544', '308545', '308549', '308551', '308553']
nosy_count = 2.0
nosy_names = ['vstinner', 'serhiy.storchaka']

priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'resource usage'
url = 'https://bugs.python.org/issue32365'
versions = ['Python 3.6', 'Python 3.7']
```

</p></details>


The following tests are leaking references: test_ast test_builtin test_compile.



Serhiy: would you mind to take a look?
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `b2a6083eb0384f38839d3f1ed32262a3852026fa` and the full history behind it is present.
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
