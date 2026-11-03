# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
it8xxx2_evb: tests/kernel/fatal/exception/ assertion failed -- "thread was not aborted"

**Describe the bug**
Test case "tests/kernel/fatal/exception/" failed on it8xxx2_evb

**To Reproduce**
Steps to reproduce the behavior:
1. west build -p always -b it8xxx2_evb tests/kernel/fatal/exception/
2. sudo -S ~/itetool/ite -f build/zephyr/zephyr.bin -s check

**Expected behavior**
The test can pass

**Impact**
daily test fail

**Logs and console output**


**Environment (please complete the following information):**
 - OS: (e.g. Linux, MacOS, Windows): Ubuntu 20.04
 - Toolchain (e.g Zephyr SDK, ...): 0.14.1



Fix the compile problem by changing
``` 
#include <zephyr/zephyr/types.h>
```
to
```
#include <zephyr/types.h>
```
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `a78e7c5c90d8cb31ec550ce289503bd698675585` and the full history behind it is present.
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
