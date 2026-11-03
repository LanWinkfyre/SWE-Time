# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
s390x RHEL7 got crash on the refleak test

link: https://buildbot.python.org/all/#/builders/217/builds/1082/steps/5/logs/stdio

`````bash

test_multiple_watchers (test.test_capi.test_watchers.TestFuncWatchers.test_multiple_watchers) ... ok
./Include/object.h:654: _Py_NegativeRefcount: Assertion failed: object has negative ref count
<object at 0x3ff7e7ffd80 is freed>
Fatal Python error: _PyObject_AssertFailed: _PyObject_AssertFailed
Python runtime state: initialized
Current thread 0x000003ff86cf7700 (most recent call first):
  Garbage-collecting
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/support/__init__.py", line 2085 in _hook
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/setup.py", line 84 in _test_audit_hook
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/test_capi/test_watchers.py", line 479 in test_watcher_raises_error
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/case.py", line 579 in _callTestMethod
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/case.py", line 623 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/case.py", line 678 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 122 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 84 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 122 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 84 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 122 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 84 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 122 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 84 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 122 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/suite.py", line 84 in __call__
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/unittest/runner.py", line 208 in run
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/support/__init__.py", line 1104 in _run_suite
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/support/__init__.py", line 1230 in run_unittest
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/runtest.py", line 281 in _test_module
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/refleak.py", line 89 in dash_R
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/runtest.py", line 315 in _runtest_inner2
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/runtest.py", line 360 in _runtest_inner
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/runtest.py", line 235 in _runtest
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/runtest.py", line 265 in runtest
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/main.py", line 353 in rerun_failed_tests
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/main.py", line 756 in _main
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/main.py", line 711 in main
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/libregrtest/main.py", line 775 in main
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/test/__main__.py", line 2 in <module>
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/runpy.py", line 88 in _run_code
  File "/home/dje/cpython-buildarea/pull_request.edelsohn-rhel-z.refleak/build/Lib/runpy.py", line 198 in _run_module_as_main
Extension modules: _testcapi, _testmultiphase, _testsinglephase, _testinternalcapi (total: 4)
make: *** [buildbottest] Aborted
program finished with exit code 2
`````

<!-- gh-linked-prs -->
### Linked PRs
* gh-102359
<!-- /gh-linked-prs -->



@erlend-aasland
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `7d1d66341838d7d1963c9ee7ffca2950d3a751fd` and the full history behind it is present.
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
