# Locate the commit that introduced this regression

A regression was reported against `etcd-io/etcd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Verification error in TestV3WatchRestoreSnapshotUnsync 

 Apart of introducing new check dedicated for data inconsistency, we also enabled previously existing check for consistent index. Based on recent weave of flakes on main branch, we have an issue.

All the failures I found happen in TestV3WatchRestoreSnapshotUnsync test:
```
logger.go:130: 2022-04-11T08:23:27.626Z	FATAL	m0	Verification failed	{"member": "m0", "data-dir": "/tmp/TestV3WatchRestoreSnapshotUnsync2779563335/002/etcd2880677907", "error": "backend.ConsistentIndex (8) must be >= last snapshot index (24)"}
```

Examples:
* https://github.com/etcd-io/etcd/runs/5968635467?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5961675211?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5961443322?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5957675983?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5956281835?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5954196012?check_suite_focus=true
* https://github.com/etcd-io/etcd/runs/5953238728?check_suite_focus=true

Our first objective is to verify the issue on `release-3.5` branch as this would impact upcoming v3.5.3 release. Second is to fix the issue on `main` branch. 



`git bisect` lead to the following commit. I will take a closer look.
```

## What you have

- `/testbed/repo` is a git clone of `etcd-io/etcd` truncated just after the regression was
  reported.  `HEAD` is `0c9a4e0f93ad9a7d83e8f5ec215baa856616c76b` and the full history behind it is present.
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
