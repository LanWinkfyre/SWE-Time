# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
explain: internal error with short-circuited post queries in EXPLAIN ANALYZE

```sql
CREATE TABLE parent (k INT PRIMARY KEY, v INT);
CREATE TABLE child (k INT PRIMARY KEY, parent_k INT REFERENCES parent(k) ON DELETE CASCADE);
EXPLAIN ANALYZE DELETE FROM parent WHERE v = 1;
```
results in
```
...
  └── • fk-cascade
        fk: child_parent_k_fkey
        error emitting plan: while building cascade plan: runtime error: invalid memory address or nil pointer dereference
```
This isn't a problem on 24.3.3 version.

Jira issue: CRDB-46446
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `04a987ecf585116bf303a6f0ff335727aa63ca1d` and the full history behind it is present.
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
