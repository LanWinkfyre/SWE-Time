# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
SIGSEGV in flb_lib_worker (flb_lib.c:909) after upgrade to 5.0.6/5.0.7 with tail input

## Bug Report

**Describe the bug**

After upgrading from fluent-bit 4.2.2 to 5.0.7 (via the fluent/fluent-bit Helm chart, chart version 0.57.7) I am experiencing issue where after few hours some of fluent-bit containers restart with `[engine] caught signal (SIGSEGV)`. 

This keeps happening as long as **tail input** is in configuration, when **tail input** is removed containers stop crashing.

Error from container log:

```bash
[2026/06/15 08:58:01] [engine] caught signal (SIGSEGV)
#0  0x56035aa43e83      in  flb_lib_worker() at src/flb_lib.c:909
#1  0x7f4adcebab7a      in  ???() at ???:0
#2  0x7f4adcf387f7      in  ???() at ???:0
#3  0xffffffffffffffff  in  ???() at ???:0
```

This is happening across 3 kubernetes clusters.

There are 3 inputs configured - tail, http and kubernetes_events.
http is used for receiving MinIO AIStor audit logs.

I've tried to keep only 1 input on each cluster to see if any of them is causing error and found out that if I remove **tail input**, crashes don't occure anymore. If I keep it in configuration, first crash appears within cca 3 hours.

Usually it's only 1 container at the time and crashes repeat, but it's not always same container crashing and it's not happening in periodic intervals.
Messages in logfile of crashed fluent-bit containers preceeding SIGSEGV are also not same across containers.

For example state of fluent-bit pods from cluster A after 1 day of runing on version 5.0.7:

```bash
NAME                       READY   STATUS    RESTARTS       AGE
logging-fluent-bit-4dj4c   1/1     Running   0              25h
logging-fluent-bit-6v26q   1/1     Running   0              25h
logging-fluent-bit-764x4   1/1     Running   0              25h
logging-fluent-bit-c47j4   1/1     Running   2 (19h ago)    25h
logging-fluent-bit-c646t   1/1     Running   0              25h
logging-fluent-bit-jq549   1/1     Running   1 (150m ago)   25h
logging-fluent-bit-zmk76   1/1     Running   5 (152m ago)   25h
...
...
```

I've tried to downgrade version-by-version while keeping **tail input** in configuration to find out which version introduces crash.

5.0.7 - crash of containers occures withing few hours, keeps repeating
5.0.6 - crash of containers occures withing few hours, keeps repeating
5.0.5 - NO crash, runs stable for over 24 hours

**Expected behavior**
I expect Fluent-bit containers not crash after update to the newest version. With same configuration we had fluent-bit running for months with older version with no crashes.

**Your Environment**
* Version used: 5.0.7 (crash), 5.0.6 (crash), 5.0.5 (no crash) deployed via fluent/fluent-bit helmchart
* k8s nodes version: v1.32.9 running with Garden Linux images
* Filters and plugins: kubernetes, lue, modify, grep, nest, record_modifier, parser, multiline, log_to_metrics

Configuration - here is configuration of inputs, I will also attach full non-default values.yaml used with helmchart deployments.


```yaml
config:
  service: |
    [SERVICE]
        Daemon Off
        Flush 1
        Grace 60
        Log_Level info
        Parsers_File /fluent-bit/etc/parsers.conf
        Parsers_File /fluent-bit/etc/conf/custom_parsers.conf
        HTTP_Server On
        HTTP_Listen 0.0.0.0
        HTTP_Port 2020
        Health_Check On
        storage.path /var/log/fluent-bit
        storage.sync normal
        storage.checksums off
        storage.max_chunks_up 128
        storage.backlog.mem_limit 10M
        storage.metrics on
        storage.delete_irrecoverable_chunks on

  inputs: |
    [INPUT]
        Name              tail
        Tag_Regex         (?<pod_name>[a-z0-9](?:[-a-z0-9]*[a-z0-9])?(?:\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*)_(?<namespace_name>[^_]+)_(?<container_name>.+)-(?<docker_id>[a-z0-9]{64})\.log$
        Tag               k8s_containers.<namespace_name>.<container_name>.<pod_name>.<docker_id>-
        Path              /var/log/containers/*.log
        Exclude_Path      /var/log/containers/mailhog*
        multiline.parser  docker, cri
        DB                /var/log/flb_kube.db
        Mem_Buf_Limit     4MB
        Skip_Long_Lines   On
        Refresh_Interval  10
        storage.type      filesystem
        storage.pause_on_chunks_overlimit On

    [INPUT]
        Name http
        Listen 0.0.0.0
        Port 9880
        Tag cluster-A-minio-audit

    [INPUT]
        Name              kubernetes_events
        Tag               k8s_events
        Interval_Sec      10
```

Full values example: [fluentbit_values.yaml](https://github.com/user-attachments/files/29054041/fluentbit_values.yaml)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4ddcb11e2689ed576487cb82d39ddf1280b610e7`.  There
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
{"case_id": "fluent_fluent_bit__11954__4ddcb11",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
