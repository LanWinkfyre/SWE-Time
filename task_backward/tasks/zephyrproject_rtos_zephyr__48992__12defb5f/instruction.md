# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
qemu_leon3: tests/posix/common/portability.posix.common fails

**Describe the bug**

The `tests/posix/common/portability.posix.common` test fails on the `qemu_leon3` target:

```
ASSERTION FAIL [0] @ WEST_TOPDIR/zephyr/kernel/sched.c:1764
	aborted _current back from dead
```

This assertion failure occurs after the test successfully completes and the test thread is aborted (fails to swap):



**To Reproduce**

Build `tests/posix/common/portability.posix.common` for `qemu_leon3` and run inside QEMU.

**Expected behavior**

Test passes.

**Impact**

CI reports a failure.

**Logs and console output**

```
Running TESTSUITE posix_apis
===================================================================
START - test_nanosleep_0_1
 PASS - test_nanosleep_0_1 in 0.020 seconds
===================================================================
START - test_nanosleep_0_1000000000
 PASS - test_nanosleep_0_1000000000 in 0.001 seconds
===================================================================
START - test_nanosleep_0_1001
 PASS - test_nanosleep_0_1001 in 0.019 seconds
===================================================================
START - test_nanosleep_0_500000000
 PASS - test_nanosleep_0_500000000 in 0.510 seconds
===================================================================
START - test_nanosleep_0_n1
 PASS - test_nanosleep_0_n1 in 0.001 seconds
===================================================================
START - test_nanosleep_1_0
 PASS - test_nanosleep_1_0 in 1.010 seconds
===================================================================
START - test_nanosleep_1_1
 PASS - test_nanosleep_1_1 in 1.020 seconds
===================================================================
START - test_nanosleep_1_1001
 PASS - test_nanosleep_1_1001 in 1.020 seconds
===================================================================
START - test_nanosleep_NULL_NULL
 PASS - test_nanosleep_NULL_NULL in 0.001 seconds
===================================================================
START - test_nanosleep_NULL_notNULL
 PASS - test_nanosleep_NULL_notNULL in 0.001 seconds
===================================================================
START - test_nanosleep_n1_0
 PASS - test_nanosleep_n1_0 in 0.001 seconds
===================================================================
START - test_nanosleep_n1_n1
 PASS - test_nanosleep_n1_n1 in 0.001 seconds
===================================================================
START - test_nanosleep_notNULL_NULL
 PASS - test_nanosleep_notNULL_NULL in 0.001 seconds
===================================================================
START - test_nanosleep_notNULL_notNULL
 PASS - test_nanosleep_notNULL_notNULL in 0.001 seconds
===================================================================
START - test_nanosleep_req_is_rem
 PASS - test_nanosleep_req_is_rem in 0.016 seconds
===================================================================
START - test_posix_clock
POSIX clock APIs
POSIX clock APIs test done
 PASS - test_posix_clock in 2.021 seconds
===================================================================
START - test_posix_mqueue
 PASS - test_posix_mqueue in 0.020 seconds
===================================================================
START - test_posix_multiple_threads_single_key

Different threads set different values to same key:
thread 0: set value = 1073897936 and retrieved value = 1073897936
thread 1: set value = 1073898160 and retrieved value = 1073898160

 PASS - test_posix_multiple_threads_single_key in 0.003 seconds
===================================================================
START - test_posix_normal_mutex
mutex lock is taken
 PASS - test_posix_normal_mutex in 0.217 seconds
===================================================================
START - test_posix_pthread_create_negative
 PASS - test_posix_pthread_create_negative in 0.001 seconds
===================================================================
START - test_posix_pthread_error_condition
 PASS - test_posix_pthread_error_condition in 0.001 seconds
===================================================================
START - test_posix_pthread_execution
Thread 0 starting with scheduling policy 0 & priority 15
Thread 1 starting with scheduling policy 0 & priority 15
Thread 2 starting with scheduling policy 0 & priority 15
Bounce test OK
Barrier test OK
 PASS - test_posix_pthread_execution in 2.795 seconds
===================================================================
START - test_posix_pthread_termination
Thread 0 starting with a priority of 4
Cancelling thread 0
Thread 1 starting with a priority of 3
Cancelling thread 1
Thread 1 could not be cancelled
Thread 2 starting with a priority of 2
Cancelling thread 2
Thread 3 starting with a priority of 1
Cancelling thread 3
Thread 3 could not be cancelled
 PASS - test_posix_pthread_termination in 1.006 seconds
===================================================================
START - test_posix_realtime
 PASS - test_posix_realtime in 2.000 seconds
===================================================================
START - test_posix_recursive_mutex
recursive mutex lock is taken
 PASS - test_posix_recursive_mutex in 0.001 seconds
===================================================================
START - test_posix_rw_lock

main acquire WR lock and 3 threads acquire RD lock
Thread 2 scheduling policy = 1 & priority 3 started
Not able to get RD lock on trying, try again
Thread 1 scheduling policy = 1 & priority 2 started
Not able to get RD lock on trying, try again
Thread 0 scheduling policy = 1 & priority 1 started
Not able to get RD lock on trying, try again
Parent thread releasing WR lock
Thread 2 got RD lock
Thread 1 got RD lock
Thread 0 got RD lock
Parent thread acquiring WR lock again
Thread 2 releasing RD lock
Thread 2 acquiring WR lock
Thread 1 releasing RD lock
Thread 1 acquiring WR lock
Thread 0 releasing RD lock
Parent thread acquired WR lock again
Thread 0 acquiring WR lock
Parent thread releasing WR lock again

3 threads acquire WR lock
Main thread acquiring RD lock
Thread 2 acquired WR lock
Thread 2 releasing WR lock
Main thread acquired RD lock
Main thread releasing RD lock
Thread 1 acquired WR lock
Thread 1 releasing WR lock
Thread 0 acquired WR lock
Thread 0 releasing WR lock
 PASS - test_posix_rw_lock in 0.139 seconds
===================================================================
START - test_posix_semaphore
 PASS - test_posix_semaphore in 5.012 seconds
===================================================================
START - test_posix_single_thread_multiple_keys

Single thread associates its value with different keys:
key 0: set value = 1073898360 and retrieved value = 1073898360
key 1: set value = 1073898360 and retrieved value = 1073898360

 PASS - test_posix_single_thread_multiple_keys in 0.002 seconds
===================================================================
START - test_posix_thread_attr_stacksize
 PASS - test_posix_thread_attr_stacksize in 0.001 seconds
===================================================================
START - test_posix_timer
POSIX timer test
Timer fires every 0 secs and  100000000 nsecs
Time remaining to fire 0 secs and  890000000 nsecs
Handler Signal value :20 for 1 times
Handler Signal value :20 for 2 times
Handler Signal value :20 for 3 times
Handler Signal value :20 for 4 times
Handler Signal value :20 for 5 times
Handler Signal value :20 for 6 times
Handler Signal value :20 for 7 times
Handler Signal value :20 for 8 times
Handler Signal value :20 for 9 times
Handler Signal value :20 for 10 times
Handler Signal value :20 for 11 times
Handler Signal value :20 for 12 times
 PASS - test_posix_timer in 2.117 seconds
===================================================================
START - test_pthread_descriptor_leak
 PASS - test_pthread_descriptor_leak in 0.011 seconds
===================================================================
TESTSUITE posix_apis succeeded

------ TESTSUITE SUMMARY START ------

SUITE PASS - 100.00% [posix_apis]: pass = 31, fail = 0, skip = 0, total = 31 duration = 18.970 seconds
 - PASS - [posix_apis.test_nanosleep_0_1] duration = 0.020 seconds
 - PASS - [posix_apis.test_nanosleep_0_1000000000] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_0_1001] duration = 0.019 seconds
 - PASS - [posix_apis.test_nanosleep_0_500000000] duration = 0.510 seconds
 - PASS - [posix_apis.test_nanosleep_0_n1] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_1_0] duration = 1.010 seconds
 - PASS - [posix_apis.test_nanosleep_1_1] duration = 1.020 seconds
 - PASS - [posix_apis.test_nanosleep_1_1001] duration = 1.020 seconds
 - PASS - [posix_apis.test_nanosleep_NULL_NULL] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_NULL_notNULL] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_n1_0] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_n1_n1] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_notNULL_NULL] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_notNULL_notNULL] duration = 0.001 seconds
 - PASS - [posix_apis.test_nanosleep_req_is_rem] duration = 0.016 seconds
 - PASS - [posix_apis.test_posix_clock] duration = 2.021 seconds
 - PASS - [posix_apis.test_posix_mqueue] duration = 0.020 seconds
 - PASS - [posix_apis.test_posix_multiple_threads_single_key] duration = 0.003 seconds
 - PASS - [posix_apis.test_posix_normal_mutex] duration = 0.217 seconds
 - PASS - [posix_apis.test_posix_pthread_create_negative] duration = 0.001 seconds
 - PASS - [posix_apis.test_posix_pthread_error_condition] duration = 0.001 seconds
 - PASS - [posix_apis.test_posix_pthread_execution] duration = 2.795 seconds
 - PASS - [posix_apis.test_posix_pthread_termination] duration = 1.006 seconds
 - PASS - [posix_apis.test_posix_realtime] duration = 2.000 seconds
 - PASS - [posix_apis.test_posix_recursive_mutex] duration = 0.001 seconds
 - PASS - [posix_apis.test_posix_rw_lock] duration = 0.139 seconds
 - PASS - [posix_apis.test_posix_semaphore] duration = 5.012 seconds
 - PASS - [posix_apis.test_posix_single_thread_multiple_keys] duration = 0.002 seconds
 - PASS - [posix_apis.test_posix_thread_attr_stacksize] duration = 0.001 seconds
 - PASS - [posix_apis.test_posix_timer] duration = 2.117 seconds
 - PASS - [posix_apis.test_pthread_descriptor_leak] duration = 0.011 seconds

------ TESTSUITE SUMMARY END ------

===================================================================
RunID: 9e2ff8b97f3a7da845c3d3a0c6ccdb19
PROJECT EXECUTION SUCCESSFUL
ASSERTION FAIL [0] @ WEST_TOPDIR/zephyr/kernel/sched.c:1764
	aborted _current back from dead
E: 
E: tt = 0x8F, trap_instruction
E: 
E:       INS        LOCALS     OUTS       GLOBALS
E:   0:  400166a0   f3000fc2   40015fa0   00000000
E:   1:  00000000   4000ebf0   000006e4   00000004
E:   2:  40016724   4000ebf4   40015fa0   00000006
E:   3:  40018000   00000004   000006e4   00000020
E:   4:  40016724   40008400   40018114   00000000
E:   5:  40015c00   f30000c0   40018000   00000100
E:   6:  400204d8   40000050   40020470   00000000
E:   7:  40006618   00000008   4000fb44   00000000
E: 
E: psr: f39000c5   wim: 00000080   tbr: 400008f0   y: 00000000
E:  pc: 40007ef4   npc: 40007ef8
E: 
E:       pc         sp
E:  #0   40007ef4   40020470
E:  #1   40006618   400204d8
E:  #2   400083d8   40020538
E:  #3   4000fcb0   00000000
E: 
E: >>> ZEPHYR FATAL ERROR 4: Kernel panic on CPU 0
E: Current thread: 0x400166a0 (unknown)
E: Halting system
```

**Environment (please complete the following information):**
 - OS: Ubuntu 20.04
 - Toolchain: Zephyr SDK 0.14.2


**Additional context**

 however this commit, in itself, does not seem to be doing anything wrong and the failure is likely due to a more serious underlying issue.

This failure is likely due to an alignment-related issue:



Changing the number of `=`s by -7 or +7 makes the assertion failure go away.

Related discussion on Discord: https://discord.com/channels/720317445772017664/733037890514321419/1007518292732289034

p.s. That this test also fails when compiled using the Zephyr SDK 0.15.0, so the issue is not toolchain or QEMU version specific.
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `f5378424f7f492a8ae0d173a015bc1186fcc7127` and the full history behind it is present.
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
