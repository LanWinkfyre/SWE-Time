# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`--experimental_add_exec_constraints_to_targets` no longer works with test targets

### Description of the bug:


Previously I was using something like `--experimental_add_exec_constraints_to_targets='\.test'=//:has_gpu` to force the matching test targets to exec on a specific remote platform in some cases. 

cc @fmeum 

I might be able to solve this use case a different way now, but still worth noting that this changed.

In my case I want some subset of targets to support 2 different modes, 1 with this constraint and 1 without it, so I add this only in specific CI workflows to make sure it gets tested on multiple exec platforms. The most obvious alternative is to use a macro to create multiple test targets that are defined with this constraint, and a negation of this constraint, but there are UX downsides to that.

### Which category does this issue belong to?

_No response_

### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.


_No response_

### Which operating system are you running Bazel on?


linux

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
  reported.  `HEAD` is `95bbed03758a7651916d0708a892f5342a0421c5` and the full history behind it is present.
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
