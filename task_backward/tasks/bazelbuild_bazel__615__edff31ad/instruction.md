# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
missing dependency declarations for standard library headers with --cpu=freebsd

I started getting the following error, when compiling with --cpu=freebsd:

ERROR: /home/f/work/bugs-bazel/BUILD:1:1: undeclared inclusion(s) in rule '//:strrev':
this rule is missing dependency declarations for the following files included by 'strrev.cc':
  '/usr/lib/clang/3.4/include/stddef.h'
  '/usr/lib/clang/3.4/include/stdarg.h'.

Not sure if it was intended that a standard library headers would produce it.

Here is a demo workspace that shows the problem.  The input command line is in the file INPUT; and the output I get is in the file OUTPUT

https://bitbucket.org/filmil/bugs-bazel/src/453cced452ad4f4e2f3ac41ee7abd9a032ed9374
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `50bf666652aacd274d534ad4ec4eadf8e8452e05` and the full history behind it is present.
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
