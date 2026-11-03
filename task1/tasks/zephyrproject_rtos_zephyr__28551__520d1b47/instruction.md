# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
up_squared: samples/boards/up_squared/gpio_counter failed.

**Describe the bug**
when running samples/boards/up_squared/gpio_counter on up_squared board, have configured the GPIO pins according to readme file, but it **reported an error "ERROR: cannot set HAT pin 37 to OUT (-22)".**

**To Reproduce**
Steps to reproduce the behavior:
1. west build -b up_squared -p auto samples/boards/up_squared/gpio_counter
2. west flash ~/up_squared.sh
3. see error

**Logs and console output**
*** Booting Zephyr OS build v2.4.0-rc2  ***
**ERROR: cannot set HAT pin 37 to OUT (-22)**


**Environment (please complete the following information):**
 - OS: Fedora31
 - Toolchain: zephyr-sdk-0.11.4
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `e01a4df3fb8d4052addf2cd8db110e7f61e09c3e` and the full history behind it is present.
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
