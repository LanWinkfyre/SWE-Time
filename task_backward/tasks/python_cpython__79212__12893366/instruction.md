# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_asyncio test_start_tls_server_1 fails in AMD64 FreeBSD CURRENT buildbots

BPO | [35031](https://bugs.python.org/issue35031)
--- | :---
Nosy | @terryjreedy, @vstinner, @tiran, @ned-deily, @asvetlov, @1st1, @pablogsal, @miss-islington, @openandclose
PRs | <li>python/cpython#10011</li><li>python/cpython#10496</li><li>python/cpython#14148</li><li>python/cpython#14150</li><li>python/cpython#14151</li><li>python/cpython#14188</li><li>python/cpython#14191</li><li>python/cpython#14192</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2019-10-14.21:07:17.113>
created_at = <Date 2018-10-20.14:06:47.648>
labels = ['3.7', '3.8', 'type-bug', 'tests', 'expert-asyncio']
title = 'test_asyncio test_start_tls_server_1 fails in AMD64 FreeBSD CURRENT buildbots'
updated_at = <Date 2019-10-14.21:07:17.112>
user = 'https://github.com/pablogsal'
```

bugs.python.org fields:
```python
activity = <Date 2019-10-14.21:07:17.112>
actor = 'vstinner'
assignee = 'none'
closed = True
closed_date = <Date 2019-10-14.21:07:17.113>
closer = 'vstinner'
components = ['Tests', 'asyncio']
creation = <Date 2018-10-20.14:06:47.648>
creator = 'pablogsal'
dependencies = []
files = []
hgrepos = []
issue_num = 35031
keywords = ['patch']
message_count = 24.0
messages = ['328138', '328143', '328145', '328148', '328157', '328163', '328833', '328835', '328837', '328839', '328871', '329785', '332756', '332764', '332803', '337234', '345831', '345832', '345837', '345839', '345961', '345967', '345973', '354654']
nosy_count = 9.0
nosy_names = ['terry.reedy', 'vstinner', 'christian.heimes', 'ned.deily', 'asvetlov', 'yselivanov', 'pablogsal', 'miss-islington', 'op368']
pr_nums = ['10011', '10496', '14148', '14150', '14151', '14188', '14191', '14192']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = 'behavior'
url = 'https://bugs.python.org/issue35031'
versions = ['Python 3.6', 'Python 3.7', 'Python 3.8']
```

</p></details>
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `0522fd81dc6e3482c2d4c8719f1f85ad5924eede` and the full history behind it is present.
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
