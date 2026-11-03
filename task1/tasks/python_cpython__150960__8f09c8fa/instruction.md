# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_logging: rotation tests fails on Windows, macOS and FreeBSD

# Bug report

* Windows PGO TailCall: https://buildbot.python.org/#/builders/1872/builds/84
* macOS NoGIL: https://buildbot.python.org/#/builders/1367/builds/1140
* FreeBSD14 Refleaks: https://buildbot.python.org/#/builders/1617/builds/886

Example on macOS:

```
FAIL: test_rollover_based_on_st_birthtime_only (test.test_logging.TimedRotatingFileHandlerTest.test_rollover_based_on_st_birthtime_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/buildbot/buildarea/pull_request.itamaro-macos-arm64-aws.macos-with-brew.refleak.nogil/build/Lib/test/test_logging.py", line 6666, in test_rollover_based_on_st_birthtime_only
    self.assertTrue(found, msg=msg)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
AssertionError: False is not true : No rotated files found, went back 5 seconds
```

Example on Windows:

```
FAIL: test_rollover_based_on_st_birthtime_only (test.test_logging.TimedRotatingFileHandlerTest.test_rollover_based_on_st_birthtime_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\bbarea\pull_request.itamaro-win64-srv-22-aws.tailcall.pgo\build\Lib\test\test_logging.py", line 6666, in test_rollover_based_on_st_birthtime_only
    self.assertTrue(found, msg=msg)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
AssertionError: False is not true : No rotated files found, went back 5 seconds

Stdout:
Contents of test_logging-2-njcaf5hh.log:
os.stat_result(st_mode=33206, st_ino=116249165381905831, st_dev=5772745545947373322, st_nlink=1, st_uid=0, st_gid=0, st_size=88, st_atime=1780658874, st_mtime=1780658874, st_ctime=1780658869)
2026-06-05 11:27:54,029 testing - new record supposedly in the new file after rollover

Contents of test_logging-2-njcaf5hh.log.2026-06-05_11-27-49:
os.stat_result(st_mode=33206, st_ino=167477611143228771, st_dev=5772745545947373322, st_nlink=1, st_uid=0, st_gid=0, st_size=123, st_atime=1780658871, st_mtime=1780658871, st_ctime=1780658869)
2026-06-05 11:27:49,817 testing - initial
2026-06-05 11:27:51,921 testing - update before rollover to renew the st_mtime


Stderr:
Test time: 2026-06-05 11-27-54
The only matching files are: ['test_logging-2-njcaf5hh.log', 'test_logging-2-njcaf5hh.log.2026-06-05_11-27-49']
```
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `e4db68b9c990ed1bb7562094bee2e73f4450d42b` and the full history behind it is present.
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
