# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql: DistSQL failing nightly logic tests

https://teamcity.cockroachdb.com/viewLog.html?tab=buildChangesDiv&buildId=532473&buildTypeId=Cockroach_SqlLogicTests

Lots of failures, like:

```
logic.go:2112: 
	/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_2.test:9194: SELECT pk, col0 FROM tab1 WHERE (col0 >= 728) AND col1 < 561.85 ORDER BY 2 DESC,1
	expected:
	    3
	    4
	    840
	    890
	    
	but found (query options: "valuesort" -> ignore the following ordering of rows) :
	
logic.go:2144: 
	/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_2.test:9202: error while processing
logic.go:2145: /go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_2.test:9202: too many errors encountered, skipping the rest of the input
```

This seems pretty messed up. There's also a few scattered panics from 10240 leftover bytes kind of things.

It's easy to reproduce locally. Run `make testlogic` and cancel once the tests start to build the `logictest.test` binary, then `cd pkg/sql/logictest`, and run:

```
./logictest.test -test.run "Test(CCL)?Logic/distsql/14.test" -bigtest -show-sql -test.v -config distsql
E180223 14:40:44.937062 163452 sql/logictest/logic.go:2139  /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby_nosort/10/slt_good_14.test:2681: too many errors encountered, skipping the rest of the input
--- total: 10032 tests, 0 failures
test logs left over in: /var/folders/wv/sn0dwhv94gz4mss7jhypx2f00000gn/T/logTestLogic267709055
--- FAIL: TestLogic (24.66s)
        test_log_scope.go:81: test logs captured to: /var/folders/wv/sn0dwhv94gz4mss7jhypx2f00000gn/T/logTestLogic267709055
        test_log_scope.go:62: use -show-logs to present logs inline
    --- FAIL: TestLogic/distsql (24.65s)
        --- PASS: TestLogic/distsql/slt_good_14.test (20.12s)
        --- FAIL: TestLogic/distsql/slt_good_14.test#01 (1.70s)
                logic.go:2112:
                        /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_14.test:1134: SELECT pk, col0 FROM tab1 WHERE ((col0 > 494)) AND col3 < 718 ORDER BY 2 DESC,1
                        expected:
                            0
                            5
                            505
                            644
                            8
                            9
                            946
                            982

                        but found (query options: "valuesort" -> ignore the following ordering of rows) :

                logic.go:2144:
                        /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_14.test:1146: error while processing
                logic.go:2145: /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby/10/slt_good_14.test:1146: too many errors encountered, skipping the rest of the input
        --- FAIL: TestLogic/distsql/slt_good_14.test#02 (2.82s)
                logic.go:2112:
                        /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby_nosort/10/slt_good_14.test:2675: SELECT pk, col0 FROM tab1 WHERE col1 = 27.90 AND col1 > 45.24 AND col0 <= 58 AND col0 < 25 AND col1 >= 13.21 OR (col0 = 32) OR (((col3 >= 18)) OR (col1 IN (72.63,82.51,16.30,42.3,29.25,31.91)) AND col0 >= 57 OR col4 > 4.80) AND col0 <= 20 ORDER BY 2 DESC,1
                        expected:
                            4
                            0

                        but found (query options: "nosort") :

                logic.go:2144:
                        /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby_nosort/10/slt_good_14.test:2681: error while processing
                logic.go:2145: /Users/jordan/go/src/github.com/cockroachdb/sqllogictest/test/index/orderby_nosort/10/slt_good_14.test:2681: too many errors encountered, skipping the rest of the input
FAIL
```

These are definitely correctness issues as we don't fail these in local SQL.
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `efdf6a2673fa7e4fc158a9138b315e021d00fc39` and the full history behind it is present.
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
