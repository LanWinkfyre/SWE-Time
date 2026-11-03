# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TestTxnCoordSenderCleanupOnAborted failing under stress

`make stress PKG=./pkg/kv TESTS=TestTxnCoordSenderCleanupOnAborted`

```
--- FAIL: TestTxnCoordSenderCleanupOnAborted (45.20s)
	txn_coord_sender_test.go:481: condition failed to evaluate within 45s: expected no heartbeat
		goroutine 41 [running]:
		runtime/debug.Stack(0xa7a358200, 0xc42096fe00, 0x68b6980)
			/Users/andrei/go/src/runtime/debug/stack.go:24 +0xa7
		github.com/cockroachdb/cockroach/pkg/testutils.SucceedsSoon(0x68e84e0, 0xc4201c4780, 0xc42096fe00)
			/Users/andrei/work/src/github.com/cockroachdb/cockroach/pkg/testutils/soon.go:38 +0x7d
		github.com/cockroachdb/cockroach/pkg/kv.verifyCleanup(0xc4202527b0, 0x1, 0x8, 0x68eb6e0, 0xc420459980, 0xc4201c4780, 0xc42096fee8, 0x2, 0x2)
			/Users/andrei/work/src/github.com/cockroachdb/cockroach/pkg/kv/txn_coord_sender_test.go:481 +0xda
		github.com/cockroachdb/cockroach/pkg/kv.TestTxnCoordSenderCleanupOnAborted(0xc4201c4780)
			/Users/andrei/work/src/github.com/cockroachdb/cockroach/pkg/kv/txn_coord_sender_test.go:678 +0x6d2
		testing.tRunner(0xc4201c4780, 0x5c39210)
			/Users/andrei/go/src/testing/testing.go:746 +0xd0
		created by testing.(*T).Run
			/Users/andrei/go/src/testing/testing.go:789 +0x2de
FAIL


ERROR: exit status 1

1946 runs completed, 1 failures, over 46s
context canceled
```
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `45ab2572599b27f0ddd456469a62470987e782a6` and the full history behind it is present.
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
