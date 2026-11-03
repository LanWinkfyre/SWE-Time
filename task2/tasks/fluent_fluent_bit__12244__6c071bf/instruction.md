# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Silent Storage Eviction Creates Untraceable "Limbo" Chunks at Info Log Level

## Bug Report

**Describe the bug**
When `storage.total_limit_size` is set on an output plugin, chunks evicted from the output queue are discarded with zero log evidence at info, warn, or error level. The only indication is a `dropped_records` metric increment.

This creates two classes of untraceable data loss at info level:

1. "Limbo chunks" — a chunk appears ONCE in the log as `failed to flush chunk 'X', retry in N seconds`, then its `task_id` is reused by a different chunk, and the original chunk name never appears again. Neither `succeeded at retry` nor `cannot be retried`. The chunk simply vanishes from the log.

2. "Silent drops" — chunks evicted from the output queue before any flush attempt is made. They produce zero log lines at all. Only the `dropped_records` metric knows they existed.

Surprisingly, chunks that are NOT silently evicted demonstrate full lifecycles in the log — `failed to flush` → retry → `succeeded at retry` or `cannot be retried`. The discrepancy makes troubleshooting impossible at info level. By the way, switching to Debug log level does not make it better. 

**To Reproduce**

Configuration:

```yaml
service:
  Flush: 1
  Log_Level: info
  storage.path: /var/log/flb-evict/
  storage.sync: normal
  storage.max_chunks_up: 64
  storage.backlog.mem_limit: 20M
  HTTP_Server: 'On'
  HTTP_Listen: 0.0.0.0
  HTTP_Port: 2020
pipeline:
  inputs:
    - name: tail
      path: /feed/*.log
      read_from_head: true
      tag: kube.evict
      storage.type: filesystem
      Mem_Buf_Limit: 500MB
      buffer_chunk_size: 32k
      buffer_max_size: 32k
      db: /var/log/flb-evict/tail.db
      Refresh_Interval: 1
  outputs:
    - name: splunk
      Match: '*'
      Host: mock-hec
      Port: 8088
      Compress: gzip
      Splunk_Token: DUMMY
      TLS: 'off'
      Retry_Limit: 3
      workers: 4
      net.max_worker_connections: 6
      storage.total_limit_size: 2M
```

1. Set up a Splunk HEC endpoint (or mock) that returns 503/error for every request with a delay (e.g., 5 second hold before returning 503). This simulates a slow/unreachable output destination.
2. Configure Fluent Bit with `storage.type: filesystem` on a tail input and `storage.total_limit_size: 2M` on the splunk output.
3. Feed records at a rate faster than the output can drain (e.g., 4000 records/sec into the tail file).
4. Observe the info-level log.
5. Query `fluentbit_output_dropped_records_total{name="splunk.0"}`.

Observed behavior (info-level log):

```
[warn] [engine] failed to flush chunk '1-1786024967.627416054.flb', retry in 9 seconds: task_id=0
[warn] [engine] failed to flush chunk '1-1786024968.628719469.flb', retry in 7 seconds: task_id=1
[warn] [engine] failed to flush chunk '1-1786024969.632756134.flb', retry in 6 seconds: task_id=2
...
[warn] [engine] failed to flush chunk '1-1786024977.327...flb', retry in 8 seconds: task_id=0  ← REUSED!
[warn] [engine] failed to flush chunk '1-1786024978.329...flb', retry in 9 seconds: task_id=1  ← REUSED!
```

No `succeeded at retry`, no `cannot be retried` for the original chunks. Their chunk names vanish from the log permanently.

Meanwhile, `dropped_records` climbs continuously.

**Expected behavior**
I was not sure how to classify this scenario. On one hand, the root cause (slow/unreachable receiver) is expected and the backpressure behavior is documented: https://docs.fluentbit.io/manual/administration/backpressure#set-storage.total_limit_size-for-output-plugins

But on the other hand, the chunk lifecycle should be traceable. If a chunk appears in the log as `failed to flush`, it has a traceable beginning — operators should be able to find its resolution too. Instead, evicted chunks have a start and then simply vanish, with no terminal log line. 

I believe the original intent of the `failed to flush chunk 'X', retry in N seconds: task_id=T` message was to help operators trace chunk lifecycles end-to-end. In reality, evicted chunks break this traceability — they disappear without any terminal message.

That is why posting as a "bug", not a "feature request".
 
**Screenshots**
No screenshots

**Your Environment**
Version used:  Fluent Bit v5.0.x / v5.1.0
Configuration: See above
Environment: Docker (reproducible)
Operating System: Linux
Plugins: tail input (filesystem storage) + Splunk output

**Additional context**
In one of our environments, I observed 100K flush failures over 5 days. Using "grep" on the info-level log, ~15K chunks had no resolvable lifecycle — they appeared once as a fail line, then vanished. I could not determine whether these ~ 15K chunks were delivered or silently dropped,  though the rest of the chunks had a resolvable lifecycle.  Delivered after 1st or 2nd retry.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6c071bf1c06079cbac09c4557264f83e381946f5`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__12244__6c071bf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
