# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash on REPL mode with long text copy and paste

BPO | [39209](https://bugs.python.org/issue39209)
--- | :---
Nosy | @vstinner, @methane, @serhiy-storchaka, @asottile, @corona10, @pablogsal, @miss-islington
PRs | <li>python/cpython#17860</li><li>python/cpython#17867</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2020-01-06.16:27:13.760>
created_at = <Date 2020-01-04.14:29:32.160>
labels = ['3.9', 'type-crash']
title = 'Crash on REPL mode with long text copy and paste'
updated_at = <Date 2020-01-06.16:27:13.760>
user = 'https://github.com/corona10'
```

bugs.python.org fields:
```python
activity = <Date 2020-01-06.16:27:13.760>
actor = 'pablogsal'
assignee = 'none'
closed = True
closed_date = <Date 2020-01-06.16:27:13.760>
closer = 'pablogsal'
components = []
creation = <Date 2020-01-04.14:29:32.160>
creator = 'corona10'
dependencies = []
files = []
hgrepos = []
issue_num = 39209
keywords = ['patch']
message_count = 5.0
messages = ['359290', '359414', '359416', '359432', '359435']
nosy_count = 7.0
nosy_names = ['vstinner', 'methane', 'serhiy.storchaka', 'Anthony Sottile', 'corona10', 'pablogsal', 'miss-islington']
pr_nums = ['17860', '17867']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'crash'
url = 'https://bugs.python.org/issue39209'
versions = ['Python 3.9']
```

</p></details>
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `7dc72b8d4f2c9d1eed20f314fd6425eab66cbc89` and the full history behind it is present.
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
