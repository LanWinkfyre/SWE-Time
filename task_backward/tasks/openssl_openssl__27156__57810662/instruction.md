# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Win32 build failing nmake test

While testing the freshly built openssl 3.6.0 with ```nmake test``` command, during test ```20-test_pkeyutl.t``` openssl was crashing. Upon connecting it to a debugger, line 1389 in ```p_lib.c``` was throwing an access violation exception because ```pkey``` was null.

Build version = VC-WIN32
MSVC version = 19.42.34438 (reported by cl.exe)
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `21f4bd986b7739f24f67270d533412065c7af0fc` and the full history behind it is present.
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
