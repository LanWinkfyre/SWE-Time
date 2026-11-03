# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
OpenAMP Sample does not work on LPCXpresso55S69

**Describe the bug**
OpenAMP sample does not correctly boot second core, so the sample stalls and the cores do not message each other.

 

**To Reproduce**
Steps to reproduce the behavior:
1. mkdir build; cd build
2. cmake -DBOARD=lpcxpresso55s69_cpu0 samples/subsys/ipc/openamp
3. make
4. Flash the image (this requires using the multicore flashing instructions [here](https://docs.zephyrproject.org/latest/boards/arm/lpcxpresso55s69/doc/index.html#building-a-dual-core-image)
5. Manually reset the board, the example will start but not get any messages from the secondary core.

**Expected behavior**
The example should run and receive messages from the `cpu1` core.

**Environment (please complete the following information):**
 - OS: Linux
 - Toolchain: Zephyr SDK
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `f8b76f3b03dec540a6aeee7b176e0f01ef2b572f` and the full history behind it is present.
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
