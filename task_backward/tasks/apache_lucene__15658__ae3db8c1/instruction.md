# Locate the commit that introduced this regression

A regression was reported against `apache/lucene`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance regression starting in Lucene 10.1.0 (dis_max + constant_score)

### Description

I observed a performance regression after upgrading Elasticsearch 8.19.8 (Lucene 9.12.3) to Elasticsearch 9.2.4 (Lucene 10.3.2). The slowdown appears for a query shape that uses dis_max + constant_score. I didn’t find any ES‑level changes that explain the regression, so I suspect Lucene.

After benchmarking performance of a query on multiple Lucene version, I confirmed a regression starting in Lucene 10.1.0.

__Query shape__

- dis_max (tie=0)
    - boost 25 * constant_score( OR of term queries on field1 + field2, minShouldMatch=1 )
    - boost 10 * constant_score( OR of term queries on field3, minShouldMatch=1 )

__Reproducer__

I created small standalone Lucene benchmark that reproduce performance regression: https://github.com/shimpeko/lucene-dismax-constantscore-benchmark

__Benchmark result (Java 25.0.2, 5k docs, warmup 200, iters 1000)__

- 9.12.3  -> 0.424 ms/iter
- 10.0.0  -> 0.439 ms/iter
- 10.1.0  -> 1.167 ms/iter
- 10.2.0  -> 1.312 ms/iter
- 10.2.1  -> 1.335 ms/iter
- 10.2.2  -> 1.345 ms/iter
- 10.3.0  -> 1.377 ms/iter
- 10.3.1  -> 1.335 ms/iter
- 10.3.2  -> 1.302 ms/iter

The regression starts at 10.1.0 and persists in later 10.x. There is also miner regression on 10.2.0

### Version and environment details

__Environment__

- OS: macOS 26.2 (Build 25C56), Darwin 25.2.0
- CPU: Apple M1 Max (10 cores: 8 performance + 2 efficiency)
- RAM: 64 GB
- Java: 25.0.2 (OpenJDK)
- Lucene directory: ByteBuffersDirectory
- Analyzer: WhitespaceAnalyzer
  - Index: 5,000 docs, single segment (forceMerge(1))
  - Searcher: single‑threaded (no executor)

__Notes__
- In ES tests,  similar query without constant_score or without dis_max did not show notable regress.


Let me know if you’d like additional data or a different reproduction setup.
```

## What you have

- `/testbed/repo` is a git clone of `apache/lucene` truncated just after the regression was
  reported.  `HEAD` is `bea2f6750e4906adcb252ea518cf21ee867c9156` and the full history behind it is present.
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
