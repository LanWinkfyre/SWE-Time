# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Code coverage collection is broken

**Code coverage collection is broken**
When running Twister using coverage reporting, it does not anymore produce LCOV output.

**To Reproduce**
Steps to reproduce the behavior:
1. `cd zephyr`
2. `twister -p native_posix -T tests/net/lib/lwm2m -c -C`
4. See error

**Expected behavior**
I would expect the Twister command above to produce a HTML file.
Instead I see error messages `lcov: ERROR: no valid records found in tracefile`

**Impact**
Cannot follow code coverage from Zephyr.

**Logs and console output**


When running on Zephyr tag `v3.0.0`, I get expected output.
```
❯ twister -p native_posix -T tests/net/lib/lwm2m -c -C
Deleting output directory /home/seta/src/ncs/zephyr/twister-out
INFO    - Zephyr version: zephyr-v3.0.0
INFO    - JOBS: 8
INFO    - Using 'zephyr' toolchain.
INFO    - Building initial testcase list...
INFO    - 4 test scenarios (4 configurations) selected, 0 configurations discarded due to filters.
INFO    - Adding tasks to the queue...
INFO    - Added initial list of jobs to queue
INFO    - Total complete:    4/   4  100%  skipped:    0, failed:    0
INFO    - 4 of 4 test configurations passed (100.00%), 0 failed, 0 skipped with 0 warnings in 29.44 seconds
INFO    - In total 99 test cases were executed, 0 skipped on 1 out of total 427 platforms (0.23%)
INFO    - 4 test configurations executed on platforms, 0 test configurations were only built.
INFO    - Generating coverage files...
INFO    - HTML report generated: /home/seta/src/ncs/zephyr/twister-out/coverage/index.html
INFO    - Saving reports...
INFO    - Writing xunit report /home/seta/src/ncs/zephyr/twister-out/twister.xml...
INFO    - Writing xunit report /home/seta/src/ncs/zephyr/twister-out/twister_report.xml...
INFO    - Run completed
```
**Environment (please complete the following information):**
 - OS: Linux
 - Toolchain Zephyr SDK 0.15.1


**Additional context**
According to Git Bisect, this commit broke the build:
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `8512bd18c66699046dffb7da0b02d72301fe8e5b` and the full history behind it is present.
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
