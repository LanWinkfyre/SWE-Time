# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_distutils: BuildRpmTestCase tests fail on RHEL buildbots

BPO | [32652](https://bugs.python.org/issue32652)
--- | :---
Nosy | @vstinner
PRs | <li>python/cpython#5303</li>

<sup>*Note: these values reflect the state of the issue at the time it was migrated and might not reflect the current state.*</sup>

<details><summary>Show more details</summary><p>

GitHub fields:
```python
assignee = None
closed_at = <Date 2018-04-25.13:27:18.575>
created_at = <Date 2018-01-24.16:35:34.562>
labels = ['3.7', 'tests']
title = 'test_distutils: BuildRpmTestCase tests fail on RHEL buildbots'
updated_at = <Date 2018-04-25.13:27:18.574>
user = 'https://github.com/vstinner'
```

bugs.python.org fields:
```python
activity = <Date 2018-04-25.13:27:18.574>
actor = 'vstinner'
assignee = 'none'
closed = True
closed_date = <Date 2018-04-25.13:27:18.575>
closer = 'vstinner'
components = ['Tests']
creation = <Date 2018-01-24.16:35:34.562>
creator = 'vstinner'
dependencies = []
files = []
hgrepos = []
issue_num = 32652
keywords = ['patch']
message_count = 3.0
messages = ['310614', '310663', '315729']
nosy_count = 1.0
nosy_names = ['vstinner']
pr_nums = ['5303']
priority = 'normal'
resolution = 'fixed'
stage = 'resolved'
status = 'closed'
superseder = None
type = None
url = 'https://bugs.python.org/issue32652'
versions = ['Python 3.7']
```

</p></details>




s390x RHEL 3.x5:

http://buildbot.python.org/all/#/builders/21/builds/577

\======================================================================
ERROR: test_no_optimize_flag (distutils.tests.test_bdist_rpm.BuildRpmTestCase)
\----------------------------------------------------------------------
```pytb
Traceback (most recent call last):
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/tests/test_bdist_rpm.py", line 120, in test_no_optimize_flag
    cmd.run()
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/command/bdist_rpm.py", line 366, in run
    self.spawn(rpm_cmd)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/cmd.py", line 365, in spawn
    spawn(cmd, search_path, dry_run=self.dry_run)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/spawn.py", line 36, in spawn
    _spawn_posix(cmd, search_path, dry_run=dry_run)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/spawn.py", line 159, in _spawn_posix
    % (cmd, exit_status))
distutils.errors.DistutilsExecError: command 'rpmbuild' failed with exit status 1
```


======================================================================
ERROR: test_quiet (distutils.tests.test_bdist_rpm.BuildRpmTestCase)
\----------------------------------------------------------------------
```pytb
Traceback (most recent call last):
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/tests/test_bdist_rpm.py", line 77, in test_quiet
    cmd.run()
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/command/bdist_rpm.py", line 366, in run
    self.spawn(rpm_cmd)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/cmd.py", line 365, in spawn
    spawn(cmd, search_path, dry_run=self.dry_run)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/spawn.py", line 36, in spawn
    _spawn_posix(cmd, search_path, dry_run=dry_run)
  File "/home/dje/cpython-buildarea/3.x.edelsohn-rhel-z/build/Lib/distutils/spawn.py", line 159, in _spawn_posix
    % (cmd, exit_status))
distutils.errors.DistutilsExecError: command 'rpmbuild' failed with exit status 1
```
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `22feeb88b473b288950cdb2f6c5d28692274b5f9` and the full history behind it is present.
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
