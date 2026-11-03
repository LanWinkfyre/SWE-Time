# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests/kernel/mem_pool/mem_pool_concept/testcase.yaml#kernel.memory_pool fails on nrf52840_pca10056, nrf52_pca10040 and  nrf51_pca10028

Execution log:
```
Running test suite mpool_concept
===================================================================
starting test - test_mpool_alloc_wait_prio

    Assertion failed at /home/kspoorth/work/latest_zephyr/tests/kernel/mem_pool/mem_pool_concept/src/test_mpool_alloc_wait.c:24: tmpool_alloc_wait_timeout: k_mem_pool_alloc(&mpool1, &block, BLK_SIZE_MIN, TIMEOUT) == -EAGAIN is false

FAIL - test_mpool_alloc_wait_prio
===================================================================
starting test - test_mpool_alloc_size_roundup

    Assertion failed at /home/kspoorth/work/latest_zephyr/tests/kernel/mem_pool/mem_pool_concept/src/test_mpool_alloc_size.c:36: test_mpool_alloc_size_roundup: k_mem_pool_alloc(&mpool1, &block[i], TEST_SIZE, K_NO_WAIT) == 0 is false

FAIL - test_mpool_alloc_size_roundup
===================================================================
starting test - test_mpool_alloc_merge_failed_diff_size
PASS - test_mpool_alloc_merge_failed_diff_size
===================================================================
starting test - test_mpool_alloc_merge_failed_diff_parent

    Assertion failed at /home/kspoorth/work/latest_zephyr/tests/kernel/mem_pool/mem_pool_concept/src/test_mpool_merge_fail_diff_parent.c:33: test_mpool_alloc_merge_failed_diff_parent: k_mem_pool_alloc(&mpool1, &block[i], BLK_SIZE_MIN, K_NO_WAIT) == 0 is false

FAIL - test_mpool_alloc_merge_failed_diff_parent
===================================================================
===================================================================
PROJECT EXECUTION FAILED
```

Steps to reproduce:
cd tests/kernel/mem_pool/mem_pool_concept
mkdir build && cd build
cmake -DBOARD=nrf51_pca10028 .. && make flash



Platforms tested: nrf52840_pca10056, nrf52_pca10040 and  nrf51_pca10028
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `d66e8077cef9c22f5dc09628ae1436a529a35472` and the full history behind it is present.
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
