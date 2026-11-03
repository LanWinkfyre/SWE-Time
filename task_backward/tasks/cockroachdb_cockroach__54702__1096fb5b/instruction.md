# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
opt: per-span cost causes regression on TPC-C

We saw a drop in TPC-C performance [on September 4th](https://roachperf.crdb.dev/?filter=&view=tpccbench%2Fnodes%3D3%2Fcpu%3D4&tab=gce). 
```
name  old warehouses  new warehouses  delta
tpcc        625 ± 4%        530 ±18%  -15.20%  (p=0.008 n=5+5)
```
 It appears that something in that PR is causing issues for TPC-C.

 The plan moves from a scan of 10 precise spans to an imprecise scan over a secondary index, a filter, and an index join. This change seems strictly worse to me. This is supported by the fact that the plan does not change in the case where we have perfectly accurate stats.

So it appears that we have a regression here in some capacity. We should have reasonably accurate stats in TPC-C, so I'd be surprised if we were using the no-stats plan, but we should confirm. Even if not, something else is going on with that PR.

Assigning the `release-blocker` tag to this for now, until it's better understood.
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `24c961f5c222bfc1b34be3fce44624c1d5aa0ad1` and the full history behind it is present.
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
