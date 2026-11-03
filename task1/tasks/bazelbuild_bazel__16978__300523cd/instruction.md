# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Status output of eagerly loaded repository rule not seen in Bazel 6 when running bazel build

### Description of the bug:


The status of repository rules that are eagerly loaded in the WORKSPACE file are not seen
when running `bazel build`


### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.


Clone https://github.com/gregmagolan/bazel_6_repo_terminal_output_repro and run `./repro.sh`


### Which operating system are you running Bazel on?


Observed on MacOS and Ubuntu

### What is the output of `bazel info release`?


release 6.0.0rc4

### If `bazel info release` returns `development version` or `(@non-git)`, tell us how you built Bazel.


_No response_

### What's the output of `git remote get-url origin; git rev-parse master; git rev-parse HEAD` ?


```text
https://github.com/gregmagolan/bazel_6_repo_terminal_output_repro
```


### Have you found anything relevant by searching the web?

Nothing

### Any other information, logs, or outputs that you want to share?

This issue affects the DX of the rules_js `npm_translate_lock` repository rule since when this invalidates it can take a noticeable amount of time to execute in repositories with a large set of npm deps.
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `0cc796aa2722bad60f314d1b27403dc0c30bf520` and the full history behind it is present.
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
