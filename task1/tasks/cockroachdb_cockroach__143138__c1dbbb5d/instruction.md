# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
perf: unknown regression in read committed benchmarks

Roachperf is reporting some regressions in several variants of YCSB and TPC-C in mid-December:

![Image](https://github.com/user-attachments/assets/723562c8-bb5c-49e1-b899-d3ffd0a6535a)

![Image](https://github.com/user-attachments/assets/f5be7eab-37bd-4b9b-a073-a60500aca5cd)

The issues seems to only impact the read committed variants of these benchmarks.

Jira issue: CRDB-48680

`buildsha.sh`

```
#!/bin/bash
set -euxo pipefail

sha=$1

git checkout $sha
./dev build --cross short
mv artifacts/cockroach-short cockroach-$sha
git checkout -

roachprod wipe tobias-ycsb
roachprod put tobias-ycsb cockroach-$sha ./cockroach
roachprod start tobias-ycsb:1-3
roachprod run tobias-ycsb:4 -- ./cockroach workload run ycsb --init --insert-count=1000000 --workload=A --concurrency=96 --splits=4 --isolation-level=read_committed {pgurl:1-3}
```

```
roachprod create -n 4 --gce-machine-type n2-standard-8 tobias-ycsb
```

Winner for the first dramatic drop is



Now I need to figure out why the recovery commit didn't recover all the way to the previous baseline.

I started a [slack thread](https://cockroachlabs.slack.com/archives/C01RX2G8LT1/p1744647833415349) to see if there's prior knowledge on this.
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `8c96475bf1e5af4a90b521ab66e34e67cc7faccc` and the full history behind it is present.
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
