# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
storage: up-replication is broken



Steps to repro:
1. Use `roachdemo` or manually start a node on localhost
2. Use `block_writer` until you have some replicas (I had 14 replicas on my node).
3. Add 2 more nodes to the cluster.
4. Wait 8 or so minutes and notice that full replication hasn't occurred.

My UI several minutes after stopping load: 
<img width="917" alt="screenshot 2016-08-02 16 22 34" src="https://cloud.githubusercontent.com/assets/1564582/17343756/56d5712c-58cd-11e6-8467-32748b2b3b6e.png">

First node logs have lots of these messages:

```
E160802 16:13:58.079597 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=11 [/Table/51/1/8066815000180517192/"f1bb11fa-d0a5-4cc2-80d9-47fb499688fa"/12442-/Max): 0 of 1 store with an attribute matching []; likely not enough nodes in cluster
E160802 16:13:58.079718 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=9 [/Table/51/1/6905099058192869454/"ba47c93d-ba45-46cf-bbca-22d8be3c0b2d"/7257-/Table/51/1/8066815000180517192/"f1bb11fa-d0a5-4cc2-80d9-47fb499688fa"/12442): 0 of 1 store with an attribute matching []; likely not enough nodes in cluster
E160802 16:13:58.079835 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=12 [/Table/51/1/5746020457527034543/"20c1db92-e9e6-4637-8e2e-f81579f18049"/23352-/Table/51/1/6905099058192869454/"ba47c93d-ba45-46cf-bbca-22d8be3c0b2d"/7257): 0 of 1 store with an attribute matching []; likely not enough nodes in cluster
E160802 16:13:58.081499 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=4 [/Table/13-/Table/14): 0 of 1 store with an attribute matching []; likely not enough nodes in cluster
E160802 16:13:58.083024 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=5 [/Table/14-/Table/50): 0 of 1 store with an attribute matching []; likely not enough nodes in cluster
E160802 16:14:44.017542 storage/queue.go:508  [replicate] (purgatory) on store=1:1 range=10 [/Table/51/1/2284333991187876666/"2e5eba36-9f26-44e7-9db2-f6ffae056f5c"/5106-/Table/51/1/3432100885105267539/"fb92fc20-73b3-41c8-a018-5606e6280922"/9173): 0 of 2 stores with an attribute matching []; likely not enough nodes in cluster
E160802 16:14:46.763930 storage/queue.go:497  [replicate] on store=1:1 range=14 [/Table/51/1/1142067297708073482/"27be8a3b-3aed-4db9-9f96-53419dcd0fa5"/8552-/Table/51/1/2284333991187876666/"2e5eba36-9f26-44e7-9db2-f6ffae056f5c"/5106): change replicas of range 14 failed: reservation declined:header:<node_id:3 store_id:3 > from_node_id:1 from_store_id:1 range_id:14 range_size:58970985
E160802 16:14:46.779365 storage/queue.go:497  [replicate] on store=1:1 range=10 [/Table/51/1/2284333991187876666/"2e5eba36-9f26-44e7-9db2-f6ffae056f5c"/5106-/Table/51/1/3432100885105267539/"fb92fc20-73b3-41c8-a018-5606e6280922"/9173): change replicas of range 10 failed: reservation declined:header:<node_id:3 store_id:3 > from_node_id:1 from_store_id:1 range_id:10 range_size:59384404
E160802 16:14:50.291948 storage/queue.go:497  [replicate] on store=1:1 range=11 [/Table/51/1/8066815000180517192/"f1bb11fa-d0a5-4cc2-80d9-47fb499688fa"/12442-/Max): change replicas of range 11 failed: context deadline exceeded
```

Long-running tasks:
<img width="339" alt="screenshot 2016-08-02 16 25 30" src="https://cloud.githubusercontent.com/assets/1564582/17343864/c52bc810-58cd-11e6-96b8-fff2d149c135.png">




cc @tamird
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `b23939d8e080250174ca5a2c25f5dd3e71df1dce` and the full history behind it is present.
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
