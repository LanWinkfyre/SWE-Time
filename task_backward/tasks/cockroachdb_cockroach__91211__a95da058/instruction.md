# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
batcheval: TestAddSSTableSSTTimestampToRequestTimestampRespectsClosedTS is flakey

```
    cmd_add_sstable_test.go:1728: 
        	Error Trace:	/home/roach/.cache/bazel/_bazel_roach/c5a4e7d36696d9cd970af2045211a7df/sandbox/processwrapper-sandbox/8031/execroot/com_github_cockroachdb_cockroach/bazel-out/k8-fastbuild/bin/pkg/kv/kvserver/batcheval/batcheval_test_/batcheval_test.runfiles/com_github_cockroachdb_cockroach/pkg/kv/kvserver/batcheval/cmd_add_sstable_test.go:1728
        	Error:      	Should not be zero, but was 0,0
        	Test:       	TestAddSSTableSSTTimestampToRequestTimestampRespectsClosedTS
```

Seen this in a recent bors run:

https://teamcity.cockroachdb.com/viewLog.html?buildId=7301543&buildTypeId=Cockroach_BazelEssentialCi

It also doesn't take too long to reproduce it if you stress the test:

```
17 runs completed, 1 failures, over 3s
```

Jira issue: CRDB-21155
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `3013bc561480c5bcabdaf0d4ae80cea717f3267e` and the full history behind it is present.
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
