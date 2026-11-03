# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ARC kernel BAT failed due to race in nested interrupts

**_Reported by Sharron LIU:_**
ARC kernel BAT failed due to recent changes made on _loapic_isr_vector_get.

how-to-reproduce
```
# cd zephyr
# source zephyr-env.sh
// x86 flashed with a simple hello world app
# make -C samples/hello_world/nanokernel/ BOARD=quark_se_devboard pristine
# make -C samples/hello_world/nanokernel/ BOARD=quark_se_devboard flash
// arc flashed with kernel BAT app (attached)
# make -C test_bat/ BOARD=quark_se_sss_devboard ARCH=arc pristine
# make -C test_bat/ BOARD=quark_se_sss_devboard ARCH=arc flash
```

expected output is BAT test complete and print message "PROJECT EXECUTION SUCCESSFUL".
actual output is BAT test blocked after printing "nano_timer: task"


(Imported from Jira ZEP-571)
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `6a1474e75b86d65e9bf2ddf7d61c076079fe89a9` and the full history behind it is present.
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
