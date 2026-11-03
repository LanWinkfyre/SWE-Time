# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test__xxsubinterpreters leaked references and memory blocks

BPO | [36447](https://bugs.python.org/issue36447)
--- | :---
Nosy | @vstinner, @ericsnowcurrently, @pablogsal
PRs | <li>python/cpython#12586</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2019-03-27.12:44:16.411>
created_at = <Date 2019-03-27.10:00:53.114>
labels = ['interpreter-core', '3.8', 'tests', 'performance']
title = 'test__xxsubinterpreters leaked references and memory blocks'
updated_at = <Date 2019-03-27.13:00:37.325>
user = 'https://github.com/pablogsal'
```

bugs.python.org fields:
```python
activity = <Date 2019-03-27.13:00:37.325>
actor = 'ZackerySpytz'
assignee = 'none'
closed = True
closed_date = <Date 2019-03-27.12:44:16.411>
closer = 'vstinner'
components = ['Interpreter Core', 'Tests']
creation = <Date 2019-03-27.10:00:53.114>
creator = 'pablogsal'
dependencies = []
files = []
hgrepos = []
issue_num = 36447
keywords = ['patch']
message_count = 3.0
messages = ['338949', '338951', '338957']
nosy_count = 3.0
nosy_names = ['vstinner', 'eric.snow', 'pablogsal']
pr_nums = ['12586']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'resource usage'
url = 'https://bugs.python.org/issue36447'
versions = ['Python 3.8']
```

</p></details>


Bisecting shows that:
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `bc284f0c7a9a7a9a4bf12c680823023a6770ce06` and the full history behind it is present.
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
