# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests: frdm_mcxn236: all application fails to run, console no output

**Describe the bug**

frdm_mcxn236 platform, all application fail to run,  

Please also mention any information which could help others to understand
the problem you're facing:
 - What target platform are you using?
 - frdm_mcxn236
 - What have you tried to diagnose or workaround this issue?
 - bisect
 - Is this a regression? If yes, have you been able to "git bisect" it to a
 - yes



**To Reproduce**

```
west update
scripts/twister --device-testing --hardware-map /home/ubuntu/nxp/frdm_mcxn236/map.yaml -T samples/hello_world/
```

**Expected behavior**

application can run

**Impact**

frdm_mcxn236 support

**Logs and console output**

when this happens no console output.


**Environment (please complete the following information):**

 - OS: (e.g. Linux, MacOS, Windows)
 - Toolchain (e.g Zephyr SDK, ...)
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `eabef50991c3aab311ea2e9f713e7510b15b9b1e` and the full history behind it is present.
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
