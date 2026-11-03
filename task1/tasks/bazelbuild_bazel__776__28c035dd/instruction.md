# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
generate_workspace doesn't work



```
dfab: /tmp/bazel $ bazel run //src/tools/generate_workspace
ERROR: /private/tmp/tp/bazel/WORKSPACE:1:6: file '/tools/build_defs/d/d.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:2:6: file '/tools/build_defs/dotnet/csharp.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:3:6: file '/tools/build_defs/jsonnet/jsonnet.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:4:6: file '/tools/build_defs/sass/sass.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:5:6: file '/tools/build_rules/go/def.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:6:6: file '/tools/build_rules/rust/rust.bzl' was not correctly loaded. Make sure the 'load' statement appears in the global scope in your file.
ERROR: /private/tmp/tp/bazel/WORKSPACE:8:1: name 'csharp_repositories' is not defined.
ERROR: /private/tmp/tp/bazel/WORKSPACE:9:1: name 'd_repositories' is not defined.
ERROR: /private/tmp/tp/bazel/WORKSPACE:10:1: name 'go_repositories' is not defined.
ERROR: /private/tmp/tp/bazel/WORKSPACE:11:1: name 'jsonnet_repositories' is not defined.
ERROR: /private/tmp/tp/bazel/WORKSPACE:12:1: name 'rust_repositories' is not defined.
ERROR: /private/tmp/tp/bazel/WORKSPACE:13:1: name 'sass_repositories' is not defined.
ERROR: Error evaluating WORKSPACE file /private/tmp/bazel/WORKSPACE.
ERROR: no such package 'external': Package 'external' contains errors.
INFO: Elapsed time: 0.046s.
ERROR: Build failed. Not running target.
```
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `8c40daa91818926460e9c917371bec74fd80c339` and the full history behind it is present.
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
