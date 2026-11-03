# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Potential memory leak in Fluentbit 4.1.1

## Bug Report

**Describe the bug**

When application is under backpressure, memory usage keeps increasing, we saw a memory footprint of 18Gi, but this could potentially keep increasing.

**To Reproduce**

Configuration file below.

**Expected behavior**

Memory usage should be much less and should be stable.

**Screenshots**


**Your Environment**
* Version used: 4.1.1
* Configuration: (Below)
* Environment name and version (e.g. Kubernetes? What version?): Kubernetes v1.31
* Server type and version:
* Operating System and version: Ubuntu 22.04
* Filters and plugins:

**Additional context**

```
[Service]
    Http_Listen    0.0.0.0
    Http_Port    2020
    Http_Server    true
    Parsers_File    /fluent-bit/etc/parsers.conf
    storage.path    /fluent-bit/tail/
    storage.backlog.mem_limit    128M
    storage.metrics    on
    storage.max_chunks_up    2048
[Input]
    Name    tail
    Buffer_Chunk_Size    5M
    Buffer_Max_Size    200M
    Path    /var/log/containers/*.log
    Skip_Long_Lines    true
    DB    /fluent-bit/tail/pos.db
    Mem_Buf_Limit    512MB
    Parser    cri
    Key    message
    Tag    kube.*
    storage.type    filesystem
    Read_from_Head    true
    Rotate_Wait    60
    Skip_Empty_Lines    true
    Threaded    true
[Input]
    Name    fluentbit_metrics
    Tag    fluentbit.metrics
    scrape_interval    5
    scrape_on_start    true
[Filter]
    Name    modify
    Match    kube.*
    Rename    log    message
[Filter]
    Name    lua
    Match    kube.*
    code    function drop_no_message_records(tag, timestamp, record) if record["message"] == nil then return -1, timestamp, record; end return 0, timestamp, record; end
    call    drop_no_message_records
[Filter]
    Name    kubernetes
    Match    kube.*
    Buffer_Size    128k
    Kube_URL    https://kubernetes.default.svc:443
    Kube_CA_File    /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    Kube_Token_File    /var/run/secrets/kubernetes.io/serviceaccount/token
    Kube_Tag_Prefix    kube.var.log.containers.
    Merge_Log    false
    K8S-Logging.Exclude    true
    Labels    false
    Annotations    false
    Use_Kubelet    false
    Namespace_Labels    true
    Namespace_Annotations    false
[Filter]
    Name    lua
    Match    kube.*
    code    function add_env_label(tag, timestamp, record) if record["kubernetes_namespace"] and record["kubernetes_namespace"]["labels"] then if record["kubernetes_namespace"]["labels"]["env"] == nil then local new_record = record; new_record["kubernetes_namespace"]["labels"]["env"] = "infra"; return 2, timestamp, new_record; end end return 0, timestamp, record; end
    call    add_env_label
[Filter]
    Name    rewrite_tag
    Match    kube.*
    Rule    $logtag .* re_emitted.$kubernetes_namespace['labels']['env'].$kubernetes['namespace_name'].$kubernetes['pod_name'].$kubernetes['container_name'] false
    Emitter_Name    re_emitted
    Emitter_Storage.type    filesystem
[Output]
    Name    prometheus_exporter
    Match    fluentbit.metrics
    Host    0.0.0.0
    Port    2021
    add_label     app    fluent-bit
    add_label     cluster    xxx
[Output]
    Name    s3
    Match    re_emitted.*
    region    eu-west-1
    bucket    xxx
    total_file_size    256M
    upload_chunk_size    50M
    upload_timeout    60m
    store_dir    /host/fluent-bit-buffer/
    s3_key_format    /archive/logs/xxx/$TAG[1]/$TAG[2]/%Y/%m/%d/%H/$TAG[3]_$TAG[4]_$INDEX.gz
    s3_key_format_tag_delimiters    .
    compression    gzip
    auto_retry_requests    true
    log_key    message
    retry_limit    10
```

<!--- How has this issue affected you? What are you trying to accomplish? -->
<!--- Providing context helps us come up with a solution that is most useful in the real world -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3a501b239fffffe199d769aaf36bb5d30fad2367`.  There
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
{"case_id": "fluent_fluent_bit__11279__3a501b2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
