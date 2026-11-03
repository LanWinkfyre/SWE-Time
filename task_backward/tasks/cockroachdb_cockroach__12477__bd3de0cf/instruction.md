# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql: regression: WINDOW partitions don't type check properly



 constants don't seem to be folded properly any more, which messes up with subsequent expression normalization. For example the query from `testdata/window`:

```sql
SELECT k, stddev(d) OVER (PARTITION BY v, 'a') FROM kv ORDER BY variance(d) OVER (PARTITION BY v, 100), k
```

now fails with a panic:

```
        panic: SELECT k, stddev(d) OVER (PARTITION BY v, 'a') FROM kv ORDER BY variance(d) OVER (PARTITION BY v, 100), k: interface conversion: *parser.StrVal is not parser.TypedExpr: missing method Eval [recovered]
[...]
panic(0x1894d80, 0xc420715e00)
        /mnt/kena/go1.7.3/src/runtime/panic.go:458 +0x243
github.com/cockroachdb/cockroach/pkg/sql/parser.(*normalizeVisitor).VisitPost(0xc4216dad70, 0x26511c0, 0xc420715ac0, 0x26511c0, 0xc420715ac0)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/parser/normalize.go:588 +0x120
github.com/cockroachdb/cockroach/pkg/sql/parser.WalkExpr(0x2643840, 0xc4216dad70, 0x26511c0, 0xc420715ac0, 0x2650d40, 0xc420f0d408, 0x2b53100)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/parser/walk.go:531 +0x1cc
github.com/cockroachdb/cockroach/pkg/sql/parser.(*FuncExpr).Walk(0xc422bf5200, 0x2643840, 0xc4216dad70, 0x1000101, 0x2650cc0)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/parser/walk.go:219 +0x1d2
github.com/cockroachdb/cockroach/pkg/sql/parser.WalkExpr(0x2643840, 0xc4216dad70, 0x2650cc0, 0xc422bf5200, 0xc422bf5200, 0x0, 0x0)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/parser/walk.go:530 +0x19e
github.com/cockroachdb/cockroach/pkg/sql/parser.(*Parser).NormalizeExpr(0xc4216da8d8, 0xc4216d97a8, 0x2655a40, 0xc422bf5200, 0x2b531a8, 0x2655a40, 0xc422bf5200, 0x0)                                                                                                                                                                                                                         
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/parser/parse.go:120 +0xc5
github.com/cockroachdb/cockroach/pkg/sql.(*planner).analyzeExpr(0xc4216d9770, 0x2650cc0, 0xc422bf4fc0, 0xc420400aa0, 0x1, 0x1, 0xc420f0d3f0, 0x7, 0x7, 0x264aa40, ...)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/analyze.go:1646 +0x13c
github.com/cockroachdb/cockroach/pkg/sql.(*planner).computeRender(0xc4216d9770, 0x2650cc0, 0xc422bf4fc0, 0x0, 0x0, 0x2654180, 0x2b531a8, 0xc420715d80, 0xc420f0d3f0, 0x7, ...)
        /mnt/kena/go/src/github.com/cockroachdb/cockroach/pkg/sql/targets.go:52 +0x245
github.com/cockroachdb/cockroach/pkg/sql.(*selectNode).initTargets(0xc422489ce0, 0xc420715c00, 0x2, 0x2, 0x0, 0x0, 0x0, 0x4, 0x200)
```
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `17b99047a726d5c3c4d8bf595812a27abdaf16ff` and the full history behind it is present.
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
