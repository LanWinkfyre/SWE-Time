# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
kvserver: TestStoreMetrics is flaky

**Describe the problem**



```
> ./dev test ./pkg/kv/kvserver --filter TestStoreMetrics --stress
...
--- FAIL: TestStoreMetrics (8.45s)
    test_log_scope.go:79: test logs captured to: /private/var/tmp/_bazel_ssd/a51ea94df2f483aee3088dde6a3dde4e/sandbox/darwin-sandbox/2148/execroot/com_github_cockroachdb_cockroach/_tmp/d5a35cf87725f62ad73d3efbbbf6e538/logTestStoreMetrics2798440868
    test_log_scope.go:80: use -show-logs to present logs inline
    client_metrics_test.go:158: gauge rocksdb.bloom.filter.prefix.checked = 0 < min 1
    client_metrics_test.go:158: gauge rocksdb.bloom.filter.prefix.useful = 0 < min 1
    client_metrics_test.go:361: -- test log scope end --
FAIL
I220525 13:20:12.118005 1 (gostd) testmain.go:1414  [-] 1  Test //pkg/kv/kvserver:kvserver_test exited with error code 1


ERROR: <nil>

5 runs completed, 1 failures, over 10s
context canceled
FAIL
```

Jira issue: CRDB-16086

 

 Should we drop the expectation further?
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `902401521dec9dacb9744a2a2389b241e05cfaa7` and the full history behind it is present.
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
