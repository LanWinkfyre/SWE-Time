# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests/crypto/mbedtls/ results in exception on frdm_k64f

The test **tests/crypto/mbedtls/** results in exception.

**Arch:** arm
**Board:** frdm_k64f


**Error Console Log:**
```
***** Booting Zephyr OS v1.12.0-rc2 *****
***** BUS FAULT *****
  Executing thread ID (thread): 0x20004138
  Faulting instruction address:  0xe1f264a0
  Stacking error
Fatal fault in essential thread! Spinning...
```

**Steps to reproduce:**
```
cd tests/crypto/mbedtls/
rm -rf build && mkdir build && cd build
cmake -D BOARD=frdm_k64f ../
make BOARD=frdm_k64f
cp zephyr/zephyr.bin /run/media/pswarnak/MBED/

Check the console log.
```



```

```
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `55494c3f0a9c9ea6ddd2ab20940dd2afafd16c71` and the full history behind it is present.
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
