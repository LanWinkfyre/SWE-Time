# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Compiling against master branch fails; error: expected expression SET_DECODE_ERROR

BPO | [32197](https://bugs.python.org/issue32197)
--- | :---
Nosy | @vstinner, @serhiy-storchaka, @CuriousLearner
PRs | <li>python/cpython#4679</li><li>python/cpython#4681</li><li>python/cpython#4694</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2017-12-04.13:06:28.532>
created_at = <Date 2017-12-02.12:50:00.715>
labels = ['build', '3.7']
title = 'Compiling against master branch fails; error: expected expression SET_DECODE_ERROR'
updated_at = <Date 2017-12-04.13:43:34.053>
user = 'https://github.com/CuriousLearner'
```

bugs.python.org fields:
```python
activity = <Date 2017-12-04.13:43:34.053>
actor = 'CuriousLearner'
assignee = 'none'
closed = True
closed_date = <Date 2017-12-04.13:06:28.532>
closer = 'vstinner'
components = []
creation = <Date 2017-12-02.12:50:00.715>
creator = 'CuriousLearner'
dependencies = []
files = []
hgrepos = []
issue_num = 32197
keywords = ['patch']
message_count = 9.0
messages = ['307427', '307429', '307443', '307444', '307452', '307559', '307562', '307563', '307566']
nosy_count = 3.0
nosy_names = ['vstinner', 'serhiy.storchaka', 'CuriousLearner']
pr_nums = ['4679', '4681', '4694']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'compile error'
url = 'https://bugs.python.org/issue32197'
versions = ['Python 3.7']
```

</p></details>
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `af5a895073c24637c094772b27526b94a12ec897` and the full history behind it is present.
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
