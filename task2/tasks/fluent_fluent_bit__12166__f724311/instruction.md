# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Expect filter does not catch all logs from batch

## Bug Report

**Describe the bug**
When opentelemetry logs come in batch, every log has a flaw, in application logs there is only information about one log.

**To Reproduce**
- docker run -p 2021:2021 --mount type=bind,src=./config.yaml,dst=/fluent-bit/etc/config.yaml fluent/fluent-bit:5.0.9 /fluent-bit/bin/fluent-bit -c /fluent-bit/etc/config.yaml
- config.yaml:
```yaml
service:
  flush: 5
  http_server: on
  health_check: on
  http_port: 2020

pipeline:
  inputs:
    - name: opentelemetry
      port: 2021

  filters:
    - name: expect
      match: '*'
      key_exists:
        - field1
        - field2
        - field3
        - field4
      action: warn

  outputs:
    - name: stdout
      match: '*'
```
- curl -H "Content-Type: application/json" -X POST -d "$(cat payload.json)" http://localhost:2021/v1/logs
- Payload:
```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "my-service"
            }
          }
        ]
      },
      "scopeLogs": [
        {
          "scope": {},
          "logRecords": [
            {
              "timeUnixNano": "1784797967000450100",
              "body": {
                "kvlistValue": {
                  "values": [
                    {
                      "key": "field1",
                      "value": {
                        "stringValue": "1"
                      }
                    },
                    {
                      "key": "field2",
                      "value": {
                        "stringValue": "2"
                      }
                    },
                    {
                      "key": "field3",
                      "value": {
                        "stringValue": "3"
                      }
                    }
                  ]
                }
              }
            },
            {
              "timeUnixNano": "1784797967000450100",
              "body": {
                "kvlistValue": {
                  "values": [
                    {
                      "key": "field1",
                      "value": {
                        "stringValue": "1"
                      }
                    },
                    {
                      "key": "field2",
                      "value": {
                        "stringValue": "2"
                      }
                    },
                    {
                      "key": "field4",
                      "value": {
                        "stringValue": "4"
                      }
                    }
                  ]
                }
              }
            },
            {
              "timeUnixNano": "1784797967000450100",
              "body": {
                "kvlistValue": {
                  "values": [
                    {
                      "key": "field1",
                      "value": {
                        "stringValue": "1"
                      }
                    },
                    {
                      "key": "field3",
                      "value": {
                        "stringValue": "3"
                      }
                    },
                    {
                      "key": "field4",
                      "value": {
                        "stringValue": "4"
                      }
                    }
                  ]
                }
              }
            },
            {
              "timeUnixNano": "1784797967000450100",
              "body": {
                "kvlistValue": {
                  "values": [
                    {
                      "key": "field2",
                      "value": {
                        "stringValue": "2"
                      }
                    },
                    {
                      "key": "field3",
                      "value": {
                        "stringValue": "3"
                      }
                    },
                    {
                      "key": "field4",
                      "value": {
                        "stringValue": "4"
                      }
                    }
                  ]
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

**Expected behavior**
Every log from the batch is logged by expect filter.

**Logs**
From 5.0.9:
```
Fluent Bit v5.0.9
* Copyright (C) 2015-2026 The Fluent Bit Authors
* Fluent Bit is a CNCF graduated project under the Fluent organization
* https://fluentbit.io

______ _                  _    ______ _ _           _____  _____ 
|  ___| |                | |   | ___ (_) |         |  ___||  _  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   _|___ \ | |/' |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / /   \ \|  /| |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V //\__/ /\ |_/ /
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/ \____(_)\___/


[2026/07/28 12:43:45.803] [ info] [fluent bit] version=5.0.9, commit=a1e05fc1f7, pid=1
[2026/07/28 12:43:45.803] [ info] [storage] ver=1.5.4, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2026/07/28 12:43:45.803] [ info] [simd    ] NEON
[2026/07/28 12:43:45.803] [ info] [cmetrics] version=2.1.5
[2026/07/28 12:43:45.803] [ info] [ctraces ] version=0.7.1
[2026/07/28 12:43:45.803] [ info] [input:opentelemetry:opentelemetry.0] initializing
[2026/07/28 12:43:45.803] [ info] [input:opentelemetry:opentelemetry.0] storage_strategy='memory' (memory only)
[2026/07/28 12:43:45.803] [ info] [input:opentelemetry:opentelemetry.0] listening on 0.0.0.0:2021 with 1 worker
[2026/07/28 12:43:45.805] [ info] [output:stdout:stdout.0] worker #0 started
[2026/07/28 12:43:45.805] [ info] [http_server] listen iface=0.0.0.0 tcp_port=2020
[2026/07/28 12:43:45.805] [ info] [sp] stream processor started
[2026/07/28 12:43:45.806] [ info] [engine] Shutdown Grace Period=5, Shutdown Input Grace Period=2
[2026/07/28 12:43:50.714] [error] [filter:expect:expect.0] exception on rule #3 'key_exists', key 'field4' not found. Record content:
{"field1":"1","field2":"2","field3":"3"}
[2026/07/28 12:43:50.714] [ warn] [filter:expect:expect.0] expect check failed
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[0] v1_logs: [[1784797967.000450100, {"otlp"=>{}}], {"field1"=>"1", "field2"=>"2", "field3"=>"3"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[1] v1_logs: [[1784797967.000450100, {"otlp"=>{}}], {"field1"=>"1", "field2"=>"2", "field4"=>"4"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[2] v1_logs: [[1784797967.000450100, {"otlp"=>{}}], {"field1"=>"1", "field3"=>"3", "field4"=>"4"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[3] v1_logs: [[1784797967.000450100, {"otlp"=>{}}], {"field2"=>"2", "field3"=>"3", "field4"=>"4"}]
^C[2026/07/28 12:44:01] [engine] caught signal (SIGINT)
[2026/07/28 12:44:01.442] [ warn] [engine] service will shutdown in max 5 seconds
[2026/07/28 12:44:01.442] [ info] [engine] pausing all inputs..
[2026/07/28 12:44:01.998] [ info] [engine] service has stopped (0 pending tasks)
[2026/07/28 12:44:01.998] [ info] [output:stdout:stdout.0] thread worker #0 stopping...
[2026/07/28 12:44:01.999] [ info] [output:stdout:stdout.0] thread worker #0 stopped
```

From 4.2.7:
```
Fluent Bit v4.2.7
* Copyright (C) 2015-2026 The Fluent Bit Authors
* Fluent Bit is a CNCF graduated project under the Fluent organization
* https://fluentbit.io

______ _                  _    ______ _ _             ___   _____ 
|  ___| |                | |   | ___ (_) |           /   | / __  \
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   __/ /| | `' / /'
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / / /_| |   / /  
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V /\___  |_./ /___
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/     |_(_)_____/
                                                                  
             Fluent Bit v4.2 – Direct Routes Ahead
         Celebrating 10 Years of Open, Fluent Innovation!

[2026/07/28 12:52:05.855843225] [ info] [fluent bit] version=4.2.7, commit=254a22f6b5, pid=1
[2026/07/28 12:52:05.855915850] [ info] [storage] ver=1.5.4, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2026/07/28 12:52:05.855927558] [ info] [simd    ] NEON
[2026/07/28 12:52:05.855928600] [ info] [cmetrics] version=1.0.6
[2026/07/28 12:52:05.855936308] [ info] [ctraces ] version=0.6.6
[2026/07/28 12:52:05.855962516] [ info] [input:opentelemetry:opentelemetry.0] initializing
[2026/07/28 12:52:05.855970141] [ info] [input:opentelemetry:opentelemetry.0] storage_strategy='memory' (memory only)
[2026/07/28 12:52:05.856120475] [ info] [input:opentelemetry:opentelemetry.0] listening on 0.0.0.0:2021
[2026/07/28 12:52:05.858662600] [ info] [output:stdout:stdout.0] worker #0 started
[2026/07/28 12:52:05.862094058] [ info] [http_server] listen iface=0.0.0.0 tcp_port=2020
[2026/07/28 12:52:05.862122808] [ info] [sp] stream processor started
[2026/07/28 12:52:05.862424516] [ info] [engine] Shutdown Grace Period=5, Shutdown Input Grace Period=2
[2026/07/28 12:52:11.311403144] [error] [filter:expect:expect.0] exception on rule #3 'key_exists', key 'field4' not found. Record content:
{"field1":"1","field2":"2","field3":"3"}
[2026/07/28 12:52:11.311418810] [ warn] [filter:expect:expect.0] expect check failed
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[0] v1_logs: [[1784797967.142924069, {"otlp"=>{}}], {"field1"=>"1", "field2"=>"2", "field3"=>"3"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[1] v1_logs: [[1784797967.142924069, {"otlp"=>{}}], {"field1"=>"1", "field2"=>"2", "field4"=>"4"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[2] v1_logs: [[1784797967.142924069, {"otlp"=>{}}], {"field1"=>"1", "field3"=>"3", "field4"=>"4"}]
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"my-service"}}, "scope"=>{}}

[3] v1_logs: [[1784797967.142924069, {"otlp"=>{}}], {"field2"=>"2", "field3"=>"3", "field4"=>"4"}]
```

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used: 5.0.9 and 4.3.7
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f724311436a1efb815d91b3672c8f4947f64755b`.  There
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
{"case_id": "fluent_fluent_bit__12166__f724311",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
