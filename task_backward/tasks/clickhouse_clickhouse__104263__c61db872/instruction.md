# Locate the commit that introduced this regression

A regression was reported against `ClickHouse/ClickHouse`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
FINAL with WHERE on PARTITION BY column reads all partitions when partition column not in primary key (regression in 26.3)

### Describe the situation

`SELECT … FINAL` with a `WHERE` predicate on the `PARTITION BY` column reads **every** partition instead of only the partitions matching the predicate, when the partition-key column is not part of the primary key. Partition pruning, the `MinMax` index, and the partition-key index are all silently skipped — `EXPLAIN indexes=1` shows `Condition: true` instead of the predicate.

### Which ClickHouse versions are affected?

- **Good:** `26.2` (and earlier through 26.1)
- **Bad:** `26.3`, `26.4`, `26.5` (master, current as of writing)

 The `skip_partition_pruning = !exprs_match && !columns_match` branch in `deferFiltersAfterFinalIfNeeded` disables partition pruning for **any** `FINAL` query whose partition-key column is not in the sorting key, regardless of whether the `WHERE` predicate is even on that column.

### How to reproduce

```sql
DROP TABLE IF EXISTS repro_final_pruning SYNC;

CREATE TABLE repro_final_pruning
(
    pk UUID,
    event_time DateTime64(3, 'UTC'),
    version UInt64
)
ENGINE = ReplacingMergeTree(version)
PARTITION BY toYYYYMM(event_time)
ORDER BY pk;

INSERT INTO repro_final_pruning SELECT generateUUIDv4(), toDateTime64('2026-01-15 00:00:00', 3, 'UTC'), 1 FROM numbers(1);
INSERT INTO repro_final_pruning SELECT generateUUIDv4(), toDateTime64('2026-02-15 00:00:00', 3, 'UTC'), 1 FROM numbers(1);
INSERT INTO repro_final_pruning SELECT generateUUIDv4(), toDateTime64('2026-03-15 00:00:00', 3, 'UTC'), 1 FROM numbers(1);
INSERT INTO repro_final_pruning SELECT generateUUIDv4(), toDateTime64('2026-04-15 00:00:00', 3, 'UTC'), 1 FROM numbers(1);
INSERT INTO repro_final_pruning SELECT generateUUIDv4(), toDateTime64('2026-05-15 00:00:00', 3, 'UTC'), 1 FROM numbers(1);

EXPLAIN indexes = 1
SELECT count() FROM repro_final_pruning FINAL
WHERE event_time >= '2026-03-01' AND event_time <= '2026-03-31';
```

`EXPLAIN indexes=1` on **26.2** (correct):

```
ReadFromMergeTree (default.repro_final_pruning)
Indexes:
  MinMax
    Keys: event_time
    Condition: and((event_time in (-Inf, '1774915200']), (event_time in ['1772323200', +Inf)))
    Parts: 1/5
    Granules: 1/5
  Partition
    Keys: toYYYYMM(event_time)
    Condition: and((toYYYYMM(event_time) in (-Inf, 202603]), (toYYYYMM(event_time) in [202603, +Inf)))
    Parts: 1/1
  PrimaryKey
    Condition: true
    Parts: 1/1
  Ranges: 1
```

`EXPLAIN indexes=1` on **26.4 / 26.5** (broken — predicate dropped):

```
ReadFromMergeTree (default.repro_final_pruning)
Indexes:
  Partition Min-Max
    Condition: true
    Parts: 5/5
    Granules: 5/5
  Partition
    Condition: true
    Parts: 5/5
  PrimaryKey
    Condition: true
    Parts: 5/5
  Ranges: 5
```

The bug also reproduces without `ReplacingMergeTree(version)` — any FINAL on a `MergeTree` family with the same partition/order shape exhibits it. Removing `FINAL` from the query restores correct pruning, so the regression is specific to the FINAL plan path.

### Expected performance

Only the partition matching the predicate should be read (1/5 parts in the synthetic, exactly as 26.2 does). On a real customer query (`SELECT … FROM t FINAL WHERE event_time BETWEEN '2026-03-01' AND '2026-03-15' GROUP BY org_id …`) this regression is **6× wall-clock and 4.4× memory**:

| | 26.2 | 26.4 |
|---|---|---|
| Duration | 24.16 s | 155.52 s |
| Memory | 1.0 GB | 4.5 GB |
| Read rows | 466 M | 1.77 B |
| Parts read | 8 / 96 | 96 / 96 |
| Result | 5 rows | identical 5 rows |

### Workaround

```sql
SETTINGS do_not_merge_across_partitions_select_final = 1
```

This forces `FINAL` to operate within partitions only and bypasses the buggy `skip_partition_pruning` path. Verified to restore 26.2-level performance and produce identical results on the affected query. Safe whenever rows with the same primary-key value cannot exist in different partitions.

### Additional context

 Even a `WHERE` purely on the partition column — which is provably safe to push to partition pruning — is dropped.

Bisected with `utils/auto-bisect/bisect.sh` over 4925 first-parent commits in 13 steps.
```

## What you have

- `/testbed/repo` is a git clone of `ClickHouse/ClickHouse` truncated just after the regression was
  reported.  `HEAD` is `79eb608ba11a1e8a832c46454143ad1e301dd097` and the full history behind it is present.
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
