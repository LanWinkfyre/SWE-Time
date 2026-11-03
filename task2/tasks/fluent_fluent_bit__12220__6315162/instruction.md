# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
`input chunk`: "no available chunk" while storage is almost empty (`fs_chunks_size` underflow)

## Bug Report

**Describe the bug**
Fluent Bit cannot create new filesystem chunks even though storage is available.
After a few hours of normal work, the `tail` input stops being able to buffer data for one
output, and these two errors repeat forever:

```
[error] [input chunk] fail to drop enough chunks in order to place new data coming from input plugin tail.1
[error] [input chunk] no available chunk
```

The storage is nearly empty at that moment: `/api/v1/storage` shows only a few chunks, and
the `storage.path` directory on the node is almost empty. The output limit is
`storage.total_limit_size: 5G`, so it is nowhere near full.

The internal counter used for that limit is corrupted. The exported capacity is a huge
negative value:
```
fluentbit_output_chunk_available_capacity_percent{name="azure_kusto_logs"} -368934881374.18988
```

Result: records are dropped, `errors` grows while `retries` stays 0, and `/api/v1/health` returns 500. 
Only a pod restart clears it, and the problem returns a few hours later.

**To Reproduce**
I tried to reproduce this with a synthetic pipeline (`dummy` input with the same
`per_record_routing` routes, `null` outputs with `storage.total_limit_size` set) and could
not trigger it.
So far I only see it on the real workload

**Expected behavior**
`fs_chunks_size` should stay in sync with what is really buffered. Ingestion should not
be blocked when the storage path is nearly empty.

## Analysis

`fs_chunks_size` is a `size_t` (unsigned) in `include/fluent-bit/flb_output.h`. If more is
subtracted than was ever added, it wraps to a value near `2^64`. The math matches with fluentbit_output_chunk_available_capacity_percent

**Your Environment**
* Version used: 5.0.9
* Environment name and version (e.g. Kubernetes? What version?): Kubernetes (AKS) 1.34.8
* Configuration:
```yaml
parsers:
  - name: customcri
    format: regex
    regex: "^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>[^ ]*) (?<log>.*)$"
    time_key: time
    time_format: "%Y-%m-%dT%H:%M:%S.%L%z"

service:
  log_level: info
  http_server: true
  health_check: true
  storage.path: /var/log/flb-storage/

pipeline:
  inputs:
    - name: fluentbit_metrics
      tag: internal_metrics
      scrape_interval: 2
      routes:
        logs:
          - name: all
            condition:
              default: true
            to:
              outputs:
                - prometheus_exporter

    - name: tail
      path: /var/log/containers/*.log
      exclude_path: /var/log/containers/fluent-bit-*.log
      parser: customcri
      multiline.parser: cri
      tag: kube.*
      storage.type: filesystem
      skip_long_lines: true
      inotify_watcher: false
      processors:
        logs:
          - name: kubernetes
            match: kube.*
            kube_url: https://kubernetes.default.svc:443
            kube_ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
            kube_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
            kube_tag_prefix: kube.var.log.containers.
            merge_log: true
            merge_log_key: log_processed
            keep_log: false

      routes:
        logs:
          - name: route_logs
            per_record_routing: true
            condition:
              op: and
              rules:
                - field: "$log_processed['EntryType']"
                  op: eq
                  value: "Type1"
            to:
              outputs:
                - azure_kusto_type1

          - name: route_metrics
            per_record_routing: true
            condition:
              op: and
              rules:
                - field: "$log_processed['EntryType']"
                  op: eq
                  value: "Type2"
            to:
              outputs:
                - azure_kusto_type2

          - name: route_traces
            per_record_routing: true
            condition:
              op: and
              rules:
                - field: "$log_processed['EntryType']"
                  op: eq
                  value: "Type3"
            to:
              outputs:
                - azure_kusto_type3

          - name: route_otel_metrics
            per_record_routing: true
            condition:
              op: and
              rules:
                - field: "$log_processed['EntryType']"
                  op: eq
                  value: "Type4"
            to:
              outputs:
                - azure_kusto_type4

  outputs:
    - name: azure_kusto
      alias: azure_kusto_type1
      tenant_id: <x>
      client_id: <x>
      client_secret: <x>
      ingestion_endpoint: <x>
      database_name: <x>
      table_name: <x>
      ingestion_mapping_reference: <name>
      buffering_enabled: true
      azure_kusto_buffer_key: azure_kusto_type1
      upload_timeout: 5m
      storage.total_limit_size: 5G

    - name: azure_kusto
      alias: azure_kusto_type2
      tenant_id: <x>
      client_id: <x>
      client_secret: <x>
      ingestion_endpoint: <x>
      database_name: <x>
      table_name: <x>
      ingestion_mapping_reference: <name>
      buffering_enabled: true
      azure_kusto_buffer_key: azure_kusto_type2
      upload_timeout: 5m
      storage.total_limit_size: 5G

    - name: azure_kusto
      alias: azure_kusto_type3
      tenant_id: <x>
      client_id: <x>
      client_secret: <x>
      ingestion_endpoint: <x>
      database_name: <x>
      table_name: <x>
      ingestion_mapping_reference: <name>
      buffering_enabled: true
      azure_kusto_buffer_key: azure_kusto_type3
      upload_timeout: 5m
      storage.total_limit_size: 2G

    - name: azure_kusto
      alias: azure_kusto_type4
      tenant_id: <x>
      client_id: <x>
      client_secret: <x>
      ingestion_endpoint: <x>
      database_name: <x>
      table_name: <x>
      ingestion_mapping_reference: <name>
      buffering_enabled: true
      azure_kusto_buffer_key: azure_kusto_type4
      upload_timeout: 5m
      storage.total_limit_size: 2G

    - name: prometheus_exporter
      match: internal_metrics
      add_label:
        - app fluent-bit
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6315162a8d4b1ef42b038834e639697f8cb44912`.  There
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
{"case_id": "fluent_fluent_bit__12220__6315162",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
