# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`class A(1, 2, 3, **d): pass` gives bad bytecode

BPO | [46161](https://bugs.python.org/issue46161)
--- | :---
Nosy | @markshannon, @sweeneyde, @zq1997
PRs | <li>python/cpython#30235</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2022-02-07.11:34:54.795>
created_at = <Date 2021-12-23.07:03:06.500>
labels = ['3.10', '3.9', 'type-crash', '3.11']
title = '`class A(1, 2, 3, **d): pass` gives bad bytecode'
updated_at = <Date 2022-02-07.11:34:54.794>
user = 'https://github.com/zq1997'
```

bugs.python.org fields:
```python
activity = <Date 2022-02-07.11:34:54.794>
actor = 'Mark.Shannon'
assignee = 'none'
closed = True
closed_date = <Date 2022-02-07.11:34:54.795>
closer = 'Mark.Shannon'
components = []
creation = <Date 2021-12-23.07:03:06.500>
creator = 'zq1997'
dependencies = []
files = []
hgrepos = []
issue_num = 46161
keywords = []
message_count = 5.0
messages = ['409069', '409073', '409079', '410813', '412734']
nosy_count = 3.0
nosy_names = ['Mark.Shannon', 'Dennis Sweeney', 'zq1997']
pr_nums = ['30235']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'crash'
url = 'https://bugs.python.org/issue46161'
versions = ['Python 3.9', 'Python 3.10', 'Python 3.11']
```

</p></details>











In debug mode, the following code gives fails a C-level assertion:

```py
d = {'metaclass': type}
for _ in [1]:
    class A(1, 2, 3, **d):
        pass
```


Assertion failed: b-\>b_startdepth \< 0 || b-\>b_startdepth == depth, file compile.c, line 6959
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `31ff96712e8f89ac1056c2da880b44650002219f` and the full history behind it is present.
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
