# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
upsquared: tests/kernel/spinlock/kernel.multiprocessing.spinlock fails.

**Describe the bug**
`tests/kernel/spinlock/kernel.multiprocessing.spinlock` fails.
`kernel.multiprocessing.spinlock`
and
`kernel.multiprocessing.spinlock.minimallibc`

**Bisect report**


**To Reproduce**
` twister --device-testing --hardware-map $HOME/up2_double.map -T tests/kernel/spinlock/ -v`

**Logs and console output**

hanlder.log contains.

```
...
    ===================================================================
    58  START - test_trylock
    59  Assertion failed at WEST_TOPDIR/zephyr/tests/kernel/spinlock/src/main.c:222: spinlock_test_trylock: trylock_failures > 0 is false
    60  FAIL - test_trylock in 1.034 seconds
    61  ===================================================================
    62  TESTSUITE spinlock failed.
    63  ------ TESTSUITE SUMMARY START ------
    64  SUITE FAIL -  85.71% [spinlock]: pass = 6, fail = 1, skip = 1, total = 8 duration = 2.112 seconds
    65  - PASS - [spinlock.test_spinlock_basic] duration = 0.001 seconds
    66  - PASS - [spinlock.test_spinlock_bounce] duration = 1.021 seconds
    67  - SKIP - [spinlock.test_spinlock_lock_time_limit] duration = 0.001 seconds
    68  - PASS - [spinlock.test_spinlock_mutual_exclusion] duration = 0.001 seconds
    69  - PASS - [spinlock.test_spinlock_no_recursive] duration = 0.018 seconds
    70  - PASS - [spinlock.test_spinlock_release_error] duration = 0.018 seconds
    71  - PASS - [spinlock.test_spinlock_unlock_error] duration = 0.018 seconds
    72  - FAIL - [spinlock.test_trylock] duration = 1.034 seconds
    73  ------ TESTSUITE SUMMARY END ------
    74  ===================================================================
    75  RunID: d685f227c8978498acdaab3119a8c20d
    76  PROJECT EXECUTION FAILED
```
```
Running TESTSUITE spinlock
===================================================================
START - test_spinlock_basic
PASS - test_spinlock_basic in 0.001 seconds
===================================================================
START - test_spinlock_bounce
PASS - test_spinlock_bounce in 0.122 seconds
===================================================================
START - test_spinlock_lock_time_limit
SKIP - test_spinlock_lock_time_limit in 0.001 seconds
===================================================================
START - test_spinlock_mutual_exclusion
PASS - test_spinlock_mutual_exclusion in 0.001 seconds
===================================================================
START - test_spinlock_no_recursive
ASSERTION FAIL [z_spin_lock_valid(l)] @ WEST_TOPDIR/zephyr/include/zephyr/spinlock.h:114
Invalid spinlock 0x59c480
Caught an assert.
Assert error expected as part of test case.
PASS - test_spinlock_no_recursive in 0.018 seconds
===================================================================
START - test_spinlock_release_error
ASSERTION FAIL [z_spin_unlock_valid(l)] @ WEST_TOPDIR/zephyr/include/zephyr/spinlock.h:287
Not my spinlock 0x59c470
Caught an assert.
Assert error expected as part of test case.
PASS - test_spinlock_release_error in 0.018 seconds
===================================================================
START - test_spinlock_unlock_error
ASSERTION FAIL [z_spin_unlock_valid(l)] @ WEST_TOPDIR/zephyr/include/zephyr/spinlock.h:240
Not my spinlock 0x59c470
Caught an assert.
Assert error expected as part of test case.
PASS - test_spinlock_unlock_error in 0.018 seconds
===================================================================
START - test_trylock
Assertion failed at WEST_TOPDIR/zephyr/tests/kernel/spinlock/src/main.c:227: spinlock_test_trylock: trylock_failures > 0 is false
FAIL - test_trylock in 1.077 seconds
===================================================================
TESTSUITE spinlock failed.
------ TESTSUITE SUMMARY START ------
SUITE FAIL -  85.71% [spinlock]: pass = 6, fail = 1, skip = 1, total = 8 duration = 1.256 seconds
- PASS - [spinlock.test_spinlock_basic] duration = 0.001 seconds
- PASS - [spinlock.test_spinlock_bounce] duration = 0.122 seconds
- SKIP - [spinlock.test_spinlock_lock_time_limit] duration = 0.001 seconds
- PASS - [spinlock.test_spinlock_mutual_exclusion] duration = 0.001 seconds
- PASS - [spinlock.test_spinlock_no_recursive] duration = 0.018 seconds
- PASS - [spinlock.test_spinlock_release_error] duration = 0.018 seconds
- PASS - [spinlock.test_spinlock_unlock_error] duration = 0.018 seconds
- FAIL - [spinlock.test_trylock] duration = 1.077 seconds
------ TESTSUITE SUMMARY END ------
===================================================================
RunID: 7999285b25c21472dff4a181a3260c24
PROJECT EXECUTION FAILED
```

**Environment (please complete the following information):**
 - OS: Linux
 - Toolchain: zephyr-sdk-0.16.0
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `f2e0f787bf83da84cd8f31d86ca214ef290c8d70` and the full history behind it is present.
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
