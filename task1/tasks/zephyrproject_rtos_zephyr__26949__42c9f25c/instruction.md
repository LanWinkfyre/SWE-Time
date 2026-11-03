# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sanitycheck gets overwhelmed by console output

**Describe the bug**
If tests have too much console output, sanitycheck gets bogged down and can't handle it all. QEMU processes spin waiting to flush their output pipes; eventually dozens of tests time out, even though they pass when built manually.

I found this in a branch I am working on which dumps out page table information to the console with ANSI color codes. With every test emitting this, sanitycheck gets overwhelmed. Many tests time out, with logs appearing truncated.

**To Reproduce**
Clone:
https://github.com/andrewboie/zephyr/tree/sanitycheck-having-a-stroke

Run sanitycheck -T tests/kernel -p qemu_x86 at a high -j level.

I think this is fairly minor as tests normally don't emit this much console data, but still the amount of data is not large and perhaps the console processing code in sanitycheck could be optimized, a modern CPU shouldn't get overwhelmed by kilobytes of data.
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `5092541e2b59f4a319520d677a59b706cd3bd665` and the full history behind it is present.
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
