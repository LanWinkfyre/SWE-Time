# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql: incorrect joins to inverted expression indexes on json equality

Inverted indexes on JSON can be used both for (a) matching within the value and (b) matching the entire value. For some reason, though, it appears that inverted indexes on JSON *expressions* can only be used for (a) matching within the value and not (b) matching the entire value. And more alarming, sometimes we're constructing the inverted join to the inverted expression index incorrectly. Here's a demonstration using `v23.2.0-alpha.2-dev`:

```sql
CREATE TABLE t (i INT PRIMARY KEY, j JSONB);
INSERT INTO t SELECT i, to_json(i % 10) FROM generate_series(0, 9999) AS s(i);
INSERT INTO t SELECT i, json_build_object('a', i % 10) FROM generate_series(10000, 19999) AS s(i);
INSERT INTO t SELECT i, json_build_object('a', json_build_object('b', i % 10)) FROM generate_series(20000, 29999) AS s(i);

-- First, test an inverted index on the column.
CREATE INVERTED INDEX ON t (j);
ANALYZE t;

-- These all use the inverted index.
EXPLAIN SELECT i FROM t WHERE j = '5';
EXPLAIN SELECT i FROM t WHERE j = '{"a": 5}';
EXPLAIN SELECT i FROM t WHERE j = '{"a": {"b": 5}}';
EXPLAIN SELECT i FROM t WHERE j->'a' = '5';
EXPLAIN SELECT i FROM t WHERE j->'a' = '{"b": 5}';
EXPLAIN SELECT i FROM t WHERE j->'a'->'b' = '5';
EXPLAIN SELECT i FROM t WHERE j @> '5';
EXPLAIN SELECT i FROM t WHERE j @> '{"a": 5}';
EXPLAIN SELECT i FROM t WHERE j @> '{"a": {"b": 5}}';
EXPLAIN SELECT i FROM t WHERE j->'a' @> '5';
EXPLAIN SELECT i FROM t WHERE j->'a' @> '{"b": 5}';
EXPLAIN SELECT i FROM t WHERE j->'a'->'b' @> '5';

-- Then, test an inverted index on (j->'a').
DROP INDEX t_j_idx;
CREATE INVERTED INDEX ON t ((j->'a'));
ANALYZE t;

-- These should all be able to use the inverted expression index, but only the last one can.
EXPLAIN SELECT i FROM t WHERE j->'a' = '5';
EXPLAIN SELECT i FROM t WHERE j->'a' = '{"b": 5}';
EXPLAIN SELECT i FROM t WHERE j->'a'->'b' = '5';

-- More concerning, these should not use the inverted expression index, but they do, and
-- get incorrect results!
EXPLAIN SELECT i FROM t WHERE j = '5';
EXPLAIN SELECT i FROM t WHERE j = '{"a": 5}';
EXPLAIN SELECT i FROM t WHERE j = '{"a": {"b": 5}}';

-- Interestingly, the cases using @> seem to behave correctly.
```

Jira issue: CRDB-32156
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `c5474dd14a5b626fbc920201bacdf19f37694c95` and the full history behind it is present.
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
