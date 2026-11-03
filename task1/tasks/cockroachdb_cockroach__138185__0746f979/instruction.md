# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql: TestDropDatabaseDeleteData failed




```
=== RUN   TestDropDatabaseDeleteData
    test_log_scope.go:165: test logs captured to: outputs.zip/logTestDropDatabaseDeleteData255376091
    test_log_scope.go:76: use -show-logs to present logs inline
    test_server_shim.go:139: cluster virtualization disabled in global scope due to issue: #76378 (expected label: C-bug)
    drop_test.go:342: condition failed to evaluate within 45s: from drop_test.go:95: descriptor exists expected=false was=true
    panic.go:626: -- test log scope end --
test logs left over in: outputs.zip/logTestDropDatabaseDeleteData255376091
--- FAIL: TestDropDatabaseDeleteData (45.90s)
```

Parameters:
 - <code>attempt=1</code>
 - <code>run=1</code>
 - <code>shard=11</code>
<details><summary>Help</summary>
<p>

See also: [How To Investigate a Go Test Failure \(internal\)](https://cockroachlabs.atlassian.net/l/c/HgfXfJgM)
</p>
</details>
/cc @cockroachdb/sql-foundations
<sub>

[This test on roachdash](https://roachdash.crdb.dev/?filter=status:open%20t:.*TestDropDatabaseDeleteData.*&sort=title+created&display=lastcommented+project) | [Improve this report!](https://github.com/cockroachdb/cockroach/tree/master/pkg/cmd/bazci/githubpost/issues)

</sub>


Jira issue: CRDB-45955
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `5207cd59f4cfd8444cb3d7739f53063bed4ae1a6` and the full history behind it is present.
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
