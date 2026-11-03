# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
os/signal: TestCtrlBreak fails on windows/386

TestCtrlBreak fails on windows/386

--- FAIL: TestCtrlBreak (2.21s)
    signal_windows_test.go:101: Program exited with error: exit status -1073741510
FAIL
FAIL    os/signal   2.280s

https://storage.googleapis.com/go-build-log/7dd1854f/windows-386-gce_0e29ac61.log

but succeeds on windows/amd64. I cannot reproduce it here. Strange.

The exit status is STATUS_CONTROL_C_EXIT. I can reproduce the failure, if I disable our C-break handler (comment out call to SetConsoleCtrlHandler in runtime).

Alex


I lied. I can reproduce it here. I did git bisect and that is what I find:





Alex
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `25bf792197ff737fc84c8b1dd46be8a6b066333a` and the full history behind it is present.
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
