# Locate the commit that introduced this regression

A regression was reported against `pingcap/tidb`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
coprocessor err: other error: unknown error StringError("offset 18446744073709551615 overflow, should be less than 2

steps to reproduce:

``` sql
CREATE TABLE `n` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

insert into n values (1),(2),(3);

analyze table n;

CREATE TABLE `v` (
  `p` int NOT NULL,
  `n` int NOT NULL,
  `v` int NOT NULL,
  `i` int NOT NULL,
  PRIMARY KEY (`p`,`i`,`n`,`v`),
  KEY `n` (`n`)
);

insert into v values (1,1,1,1);

analyze table v;

select n.id from v join n on n.id = v.n where p=1 and n.id in (select n from v where p=1);
```

```
2018/01/07 11:12:09.741 column.go:339: [error] Can't find column test.v1.p1 in schema Column: [,] Unique key: []
2018/01/07 11:12:09.831 coprocessor.go:613: [warning] coprocessor err: other error: unknown error StringError("offset 18446744073709551615 overflow, should be less than 2")
2018/01/07 11:12:09.832 coprocessor.go:613: [warning] coprocessor err: other error: unknown error StringError("offset 18446744073709551615 overflow, should be less than 2")
2018/01/07 11:12:09.842 coprocessor.go:613: [warning] coprocessor err: other error: unknown error StringError("offset 18446744073709551615 overflow, should be less than 2")
2018/01/07 11:12:09.843 conn.go:470: [warning] [1] dispatch error:
id:1, addr:192.168.20.8:42504 status:2, collation:utf8_general_ci, user:root
/go/src/github.com/pingcap/tidb/store/tikv/coprocessor.go:612: other error: unknown error StringError("offset 18446744073709551615 overflow, should be less than 2")
/go/src/github.com/pingcap/tidb/store/tikv/coprocessor.go:614: 
/go/src/github.com/pingcap/tidb/store/tikv/coprocessor.go:515: 
/go/src/github.com/pingcap/tidb/store/tikv/coprocessor.go:495: 
/go/src/github.com/pingcap/tidb/distsql/distsql.go:108: 
/go/src/github.com/pingcap/tidb/distsql/distsql.go:178: 
/go/src/github.com/pingcap/tidb/distsql/distsql.go:159: 
/go/src/github.com/pingcap/tidb/executor/distsql.go:179: 
/go/src/github.com/pingcap/tidb/executor/distsql.go:624: 
/go/src/github.com/pingcap/tidb/executor/distsql.go:862: 
/go/src/github.com/pingcap/tidb/executor/distsql.go:837: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:493: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:387: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:369: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:267: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:230: 
/go/src/github.com/pingcap/tidb/executor/new_index_lookup_join.go:181: 
/go/src/github.com/pingcap/tidb/executor/sort.go:497: 
/go/src/github.com/pingcap/tidb/executor/sort.go:471: 
/go/src/github.com/pingcap/tidb/executor/executor.go:639: 
/go/src/github.com/pingcap/tidb/executor/adapter.go:106: 
/go/src/github.com/pingcap/tidb/server/conn.go:938: 
/go/src/github.com/pingcap/tidb/server/conn.go:863: 
/go/src/github.com/pingcap/tidb/server/conn.go:824: 
```




 
@hanfei1991  mind take a look?
  


Tikv version used:
```
TiKV 
Release Version:   1.0.1
Git Commit Hash:   1de37670ee601deba5d88609dcd7d848de2a11e3
Git Commit Branch: master
UTC Build Time:    2018-01-06 03:16:59
Rust Version:      1.24.0-nightly (b98fd524e 2018-01-05)
```
```

## What you have

- `/testbed/repo` is a git clone of `pingcap/tidb` truncated just after the regression was
  reported.  `HEAD` is `ecbd60c3fffd76ed46613da0be89ead4bda7e06c` and the full history behind it is present.
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
