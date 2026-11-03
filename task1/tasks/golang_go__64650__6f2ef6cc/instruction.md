# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: frequent TestCrashDumpsAllThreads failures on `linux/s390x`

```
#!watchflakes
post <- goarch == "s390x" && pkg == "runtime" && test == "TestCrashDumpsAllThreads"
```

### Go version



### What operating system and processor architecture are you using (`go env`)?




### What did you do?

https://build.golang.org/log/5e29be06bbb7a8a4923d83a58972aa2a10677a94

### What did you expect to see?

All tests passing.

### What did you see instead?

```
--- FAIL: TestCrashDumpsAllThreads (0.11s)
    crash_unix_test.go:145: found 2 instances of main.crashDumpsAllThreadsLoop; expected 4
…
FAIL
FAIL	runtime	46.511s
```

(attn @golang/s390x)
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `ba7c4e47b32fa99db8aa05331426b328bb39517a` and the full history behind it is present.
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
