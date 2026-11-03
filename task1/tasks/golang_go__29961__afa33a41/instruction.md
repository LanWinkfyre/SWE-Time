# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: scheduler randomness lost

<!-- Please answer these questions before submitting your issue. Thanks! -->

### What version of Go are you using (`go version`)?
1.12 beta 2

### Does this issue reproduce with the latest release?
Only seeing it with 1.12 beta 2

### What operating system and processor architecture are you using (`go env`)?
GOARCH="amd64"
GOOS="darwin"

### What did you do?
I've been using this program in training for years. It shows how random the scheduler is with context switches and it can't be predicted.

https://github.com/ardanlabs/gotraining/blob/master/topics/go/concurrency/goroutines/example2/example2.go

Just build the program and run it several times. On 1.11 or earlier, you will see the B goroutine context switches as an unpredictable prime number each time. Sometimes you get 4 context switches before it is complete. It is very rare not to get one before the work for any goroutine is complete. On 1.12, these context switches are gone. I am seeing this behavior with other programs I have. This one is the easiest to run and see the change.

### What did you expect to see?

Create Goroutines
Waiting To Finish
B:2
B:3
B:5
B:7
. . .
B:4139
B:4153
B:4157
A:2 <- Unpredictable context switch
A:3
A:5
A:7
. . .
A:4231
A:4241
A:4243
B:4159 <- Unpredictable context switch
B:4177
B:4201
. . .
Completed B
. . .
A:4987
A:4993
A:4999
Completed A

### What did you see instead?
Every time I run it there is no context switch. The B goroutine finishes completely and then the A goroutine runs. This happens every single time.

B:2
B:3
B:5
B:7
B:11
...
B:4987
B:4993
B:4999
Completed B
A:2
A:3
A:5
A:7
. . .
A:4987
A:4993
A:4999
Completed A


I was curious after seeing this issue, and was able to reproduce this on my machine (comparing `master` and 1.11.5 with `example2.go`), so I did a bisect. Maybe unsurprisingly...
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `447965d4e008764a8635df6ca7d5d2e59c6d4229` and the full history behind it is present.
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
