# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
X86 kernel BAT failed:  Kernel Allocation Failure!

**_Reported by Sharron LIU:_**
X86 kernel BAT failed.

how-to-reproduce
```
# cd zephyr
# source zephyr-env.sh
// x86 flashed with kernel BAT app (attached)
# make -C test_bat/ BOARD=quark_se_devboard pristine
# make -C test_bat/ BOARD=quark_se_devboard flash
```

expected output is BAT test complete and print message "PROJECT EXECUTION SUCCESSFUL".
actual output is BAT test printing "**** Kernel Allocation Failure! ****"
```
tc_start() - BAT: microkernel
timer: task
memory map: task
memory pool: task
event: task-fiber
event: task-isr
event: task-task
sema: task-fiber
sema: task-isr
mutex: task-task
fifo: task-task
mailbox: task-task
**** Kernel Allocation Failure! ****
Current thread ID = 0xa8008c20
Faulting segment:address = 0x0000dead:0xdeaddead
eax: 0xdeaddead, ebx: 0xdeaddead, ecx: 0xdeaddead, edx: 0xdeaddead
esi: 0xdeaddead, edi: 0xdeaddead, ebp: 0deaddead, esp: 0xdeaddead
eflags: 0xdeaddead
Fatal essential fiber error! Spinning...
```


(Imported from Jira ZEP-572)
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `1de77488ae543b119524cbc14344020c9f2eb43f` and the full history behind it is present.
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
