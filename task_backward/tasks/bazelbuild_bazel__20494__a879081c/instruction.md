# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bazel 7 no longer allow `label_flag` used as constraint values for platforms

### Description of the bug:


With Bazel 7 it seems one can no longer use a `label_flag` target when a constraint value is expected. I keep getting the following error

```
ERROR: /Users/tgeng/tmp/bazel-label-flag/BUILD:1:9: in constraint_values attribute of platform rule //:target_base: '//:target_cpu' does not have mandatory providers: 'ConstraintValueInfo'
```

### Which category does this issue belong to?


_No response_

### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.


The following works with Bazel 6.4.0

```
~/tmp/workspace $ cat BUILD
platform(
    name = "target_base",
    constraint_values = ["target_cpu"],
)

label_flag(
    name = "target_cpu",
    build_setting_default = "@platforms//cpu:arm",
)
~/tmp/workspace $ bazel build //:target_base
INFO: Analyzed target //:target_base (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:target_base up-to-date (nothing to build)
INFO: Elapsed time: 0.074s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
```
But with Bazel 7 I have the following error:
```
~/tmp/workspace $ bazel build //:target_base
Starting local Bazel server and connecting to it...
ERROR: /Users/tgeng/tmp/bazel-label-flag/BUILD:1:9: in constraint_values attribute of platform rule //:target_base: '//:target_cpu' does not have mandatory providers: 'ConstraintValueInfo'
ERROR: /Users/tgeng/tmp/bazel-label-flag/BUILD:1:9: Analysis of target '//:target_base' failed
ERROR: Analysis of target '//:target_base' failed; build aborted
INFO: Elapsed time: 2.021s, Critical Path: 0.02s
INFO: 1 process: 1 internal.
ERROR: Build did NOT complete successfully
```

### Which operating system are you running Bazel on?


macOS, Linux

### What is the output of `bazel info release`?


release 7.0.0

### If `bazel info release` returns `development version` or `(@non-git)`, tell us how you built Bazel.


_No response_

### What's the output of `git remote get-url origin; git rev-parse master; git rev-parse HEAD` ?


_No response_

### Is this a regression? If yes, please try to identify the Bazel commit where the bug was introduced.


I tried running bisect but it failed.


### Have you found anything relevant by searching the web?

_No response_

### Any other information, logs, or outputs that you want to share?

_No response_

I bisected with `bazelisk --bisect=6.4.0..HEAD build //:target_base` to avoid the problematic commit (that is also being fixed so --bisect=6.4.0..7.0.0 could also work in about ~30 mins).



/cc @katre , is this a intended breaking change or a regression in Bazel 7?
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `47e48a13563742473abdcaef46b7c4f222a86831` and the full history behind it is present.
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
