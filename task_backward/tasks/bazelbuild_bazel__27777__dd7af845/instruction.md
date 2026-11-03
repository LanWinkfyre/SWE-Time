# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bazel interrupts itself and exits with dynamic execution

### Description of the bug:


sometimes build act like they ctrl-c'd themselves with this message:

```
INFO: Checking for file changes...
INFO: Analyzed target //:whatever (0 packages loaded, 0 targets configured).
Target //:whatever failed to build
Use --verbose_failures to see the command lines of failed build steps.
ERROR: build interrupted
INFO: Elapsed time: 4.928s, Critical Path: 2.96s
INFO: 692 processes: 17 disk cache hit, 2 remote cache hit, 673 internal.
ERROR: Build did NOT complete successfully
ERROR: Build failed. Not running target
```

I was able to build bazel printing the stack trace in this case:



### Which category does this issue belong to?

_No response_

### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.


_No response_

### Which operating system are you running Bazel on?


_No response_

### What is the output of `bazel info release`?




### If `bazel info release` returns `development version` or `(@non-git)`, tell us how you built Bazel.


_No response_

### What's the output of `git remote get-url origin; git rev-parse HEAD` ?


```text

```

### If this is a regression, please try to identify the Bazel commit where the bug was introduced with bazelisk --bisect.


_No response_

### Have you found anything relevant by searching the web?

_No response_

### Any other information, logs, or outputs that you want to share?

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `25f91f948a84de1b9158dea8904a98b671e76ed5` and the full history behind it is present.
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
