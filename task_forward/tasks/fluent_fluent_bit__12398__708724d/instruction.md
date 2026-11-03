# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[downstream] connection #X from timed out after ... seconds appears intermittently after upgrading to v5.0.8 (HTTP input)

After upgrading from Fluent Bit v4.2.2 to v5.0.8, our `log-proxy` service (which uses the `http` input to receive logs from other Fluent Bit clients and send them to Kafka) began logging intermittent errors:
```
[error] [downstream] connection #47 from timed out after 10 seconds (IO timeout)
```
The error did not exist in v4.x with the same architecture. It appears sporadically, at random times, with no correlated client-side errors, no restarts, and no apparent impact on log consistency or delivery. Debug logging provides no additional context. We tried adjusting `net.io_timeout` to 60s/120s/180s, but the error still occurs (the timeout value reported in the error message changed to match the configured value - e.g., "timed out after 60 seconds").

We are unsure whether this parameter is even the correct knob for this behavior in v5.0, or whether this is a regression in the refactored HTTP listener stack. We'd like to determine the root cause of this new error and whether it is a bug or an expected side effect of v5.0's architectural changes.

Configuration:

```yaml
service:
  flush: 1
  daemon: off
  log_level: ${LOG_LEVEL}
  parsers_file: /config/parsers.yaml
  http_listen: 0.0.0.0
  http_port: 2020
  storage.path: /fbstorage
  storage.sync: normal
  storage.checksum: off
  storage.max_chunks_up: 128
  storage.backlog.mem_limit: 10M
  storage.metrics: on
  net.dns.mode: UDP

pipeline:
  inputs:
  - name: http
    host: 0.0.0.0
    port: 8080
    http_server.buffer_max_size: 10M
    http_server.buffer_chunk_size: 512K
    net.io_timeout: 60s
    storage.type: filesystem
  filters:
  - name: lua
    match_regex: .*
    script: /config/timestamp.lua
    call: fix_timestamp_clickhouse
  outputs:
  - name: kafka
    match: '*'
    log_level: info
    brokers: egress-kafkase.k8s-namespace-name.svc.cluster.local:19093
    topics: dev_logs
    format: json
    timestamp_format: iso8601
    timestamp_key: timestamp_kafka
    retry_limit: False
    rdkafka.broker.address.family: v4
    rdkafka.message.send.max.retries: 1
    rdkafka.retry.backoff.ms: 100
    rdkafka.request.required.acks: all
    rdkafka.request.timeout.ms: 2000
    storage.total_limit_size: 400M
```

Environment:
- Fluent Bit version: 5.0.8
- Deployment: Kubernetes (K8s) + Istio service mesh in the sidecar mode; both log-proxy and the client applications are deployed in the same namespace, log-proxy sends logs to Kafka, the client applications send logs to log-proxy
- Previous version: 4.2.2
- Client setup: the client (downstream) applications are also on v5.0.8 and use the `http` output to send logs to `log-proxy:8080`
```yaml
service:
  flush: 5
  daemon: off
  log_level: info
  parsers_file: /config/parsers.yaml
  http_server: on
  http_listen: 0.0.0.0
  http_port: 2020
  storage.path: /fbstorage
  storage.sync: normal
  storage.checksum: off
  storage.max_chunks_up: 128
  storage.backlog.mem_limit: 10M
  storage.metrics: on
  net.dns.mode: UDP

pipeline:
  inputs:
#...
  filters:
#...

  outputs:
  - name: http
    match_regex: (pilot.*|.*stdout|.*stderr|.*sysout)
    log_level: info
    retry_limit: 1
    host: log-proxy
    port: 8080
    format: json
    json_date_key: '@timestamp'
    json_date_format: iso8601
    storage.total_limit_size: 90M
    workers: 2
```
<details>
<summary>Logs</summary>
Starting application
Fluent Bit v5.0.8
* Copyright (C) 2015-2026 The Fluent Bit Authors
* Fluent Bit is a CNCF graduated project under the Fluent organization
* https://fluentbit.io

______ _                  _    ______ _ _           _____  _____ 
|  ___| |                | |   | ___ (_) |         |  ___||  _  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   _|___ \ | |/' |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / /   \ \|  /| |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V //\__/ /\ |_/ /
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/ \____(_)\___/


[2026/08/19 14:52:31.493] [ info] [fluent bit] version=5.0.8, commit=, pid=1
[2026/08/19 14:52:31.493] [ info] [storage] ver=1.5.4, type=memory+filesystem, sync=normal, checksum=off, max_chunks_up=128
[2026/08/19 14:52:31.493] [ info] [storage] backlog input plugin: storage_backlog.1
[2026/08/19 14:52:31.493] [ info] [simd    ] SSE2
[2026/08/19 14:52:31.493] [ info] [cmetrics] version=2.1.5
[2026/08/19 14:52:31.493] [ info] [ctraces ] version=0.7.1
[2026/08/19 14:52:31.493] [ info] [input:http:http.0] initializing
[2026/08/19 14:52:31.493] [ info] [input:http:http.0] storage_strategy='filesystem' (memory + filesystem)
[2026/08/19 14:52:31.493] [ info] [input:http:http.0] listening on 0.0.0.0:8080 with 1 worker
[2026/08/19 14:52:31.493] [ info] [input:storage_backlog:storage_backlog.1] initializing
[2026/08/19 14:52:31.493] [ info] [input:storage_backlog:storage_backlog.1] storage_strategy='memory' (memory only)
[2026/08/19 14:52:31.493] [ info] [input:storage_backlog:storage_backlog.1] queue memory limit: 9.5M
[2026/08/19 14:52:31.496] [ info] [output:kafka:kafka.0] brokers='egress-kafkase.k8s-namespace-name.svc.cluster.local:19093' topics='dev_logs'
[2026/08/19 14:52:31.500] [ info] [http_server] listen iface=0.0.0.0 tcp_port=2020
[2026/08/19 14:52:31.500] [ info] [sp] stream processor started
[2026/08/19 14:52:31.500] [ info] [engine] Shutdown Grace Period=5, Shutdown Input Grace Period=2
[2026/08/19 14:54:59.042] [error] [downstream] connection #51 from  timed out after 60 seconds (IO timeout)
[2026/08/19 14:57:45.542] [error] [downstream] connection #57 from  timed out after 60 seconds (IO timeout)
[2026/08/19 14:59:30.542] [error] [downstream] connection #53 from  timed out after 60 seconds (IO timeout)
[2026/08/19 14:59:50.042] [error] [downstream] connection #51 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:00:00.542] [error] [downstream] connection #55 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #32 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #56 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #62 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #50 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #73 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #55 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:01:15.542] [error] [downstream] connection #58 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:04:00.544] [error] [downstream] connection #52 from  timed out after 60 seconds (IO timeout)
[2026/08/19 15:04:00.544] [error] [downstream] connection #63 from  timed out after 60 seconds (IO timeout)
</details>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `708724d97f6ce96a65b97d8330d6d38469ca745a`.  There
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
{"case_id": "fluent_fluent_bit__12398__708724d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
