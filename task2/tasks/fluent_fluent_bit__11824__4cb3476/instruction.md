# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Fluentbit Loki output Tenant_Id_Key routing not working properly.

## Bug Report

**Describe the bug**
<!--- A clear and concise description of what the bug is. -->
Fluentbit version: 5.0.3
EKS version: 1.30
Fluentbit deployment mode: Daemonset

I am performing POC to replace the promtail by fluentbit for Loki stack. In my current setup, I am using multi-cluster with multi tenant <clucstername>-<namespace> using dynamic tenancy in Promtail. While performing POC with promtail, the resource utilisation is very less at scale and very impressive but get blocked at tenancy behaviour. I see there is option to set Tenant_Id_Key <Key> to support multi tenant dynamic mode but observed It's intermittently adding different tenant log in different tenant causes inconsistent loglines for any tenant. 

**To Reproduce**
- Rubular link if applicable:
- I am using below config for Log pipeline from ref https://docs.fluentbit.io/manual/data-pipeline/outputs/loki .
```
  inputs: |
    [INPUT]
        Name tail
        Path /var/log/containers/*.log
        Tag kube.*
        Mem_Buf_Limit 25MB
        Skip_Long_Lines Off
        multiline.parser  docker, cri
  filters: |
    [FILTER]
        Name kubernetes
        Match kube.*
        Merge_Log On
        Keep_Log Off
        K8S-Logging.Parser On
        K8S-Logging.Exclude On

    [FILTER]
        Name parser
        Match kube.*
        Key_Name log
        Parser json
        Reserve_Data On

    [FILTER]
        Name lua
        Match kube.*
        script /fluent-bit/etc/conf/log_pipeline.lua
        call enrich_log

    # Group records by namespace before Loki output flush.
    [FILTER]
        Name rewrite_tag
        Match kube.*
        Rule $tenant_id ^(.+)$ loki.$1 false
        Emitter_Name re_emitted

  ## https://docs.fluentbit.io/manual/pipeline/outputs
  outputs: |
    [OUTPUT]
        Name Loki
        Match loki.*
        Host loki-distributor.observability.svc.cluster.local
        Uri /loki/api/v1/push
        Port 3100
        Line_Format key_value
        Drop_Single_Key raw
        Tenant_Id_Key tenant_id
        workers 0
        Retry_Limit False
        Labels agent=fluentbit,cluster_name=qa,deployed_on=k8s
        Label_Map_Path /fluent-bit/etc/conf/loki_label_map.json
        Remove_keys kubernetes,app,level,tenant_id

      Lua function for tenant_id label
    
     function enrich_log(tag, timestamp, record)
        local k8s = record["kubernetes"] or {}
        local out = {}
        out["kubernetes"] = k8s
        out["tenant_id"] = k8s["namespace_name"] or "default"
```
- Example log message if applicable:
```

2026-05-19 17:07:38.828 | I0519 11:37:38.828040       1 topology.go:175] "Skipping topology aware endpoint filtering since one or more endpoints is missing a zone hint" endpoint="172.16.82.162:3000" 

Fields
  | I | __tenant_id__ | revenue
  | I | agent | fluentbit
  | I | app | unknown
  | I | cluster_name | qa
  | I | container_name | kube-proxy
  | I | deployed_on | k8s
  | S | detected_level | info
  | I | level | info
  | I | namespace | kube-system
  | I | pod | kube-proxy-sqdfb
  | I | service_name | unknown


```
- Steps to reproduce the problem:
1: Deploy the Fluentbit as  Daemonset mode on multiple EKS nodes with tail input.
2: Use namespace for Tenant_Id_Key for Loki output plugin.
3: Crearte datasource for a single tennat datasource on grafana and list the namespaces, even we have specified a single namespace tenant still the intermittent data is getting pushed in wrong tenant.

**Expected behavior**
<!--- A clear and concise description of what you expected to happen. -->
 - Each tenantkey <namespace> should contain logs of the specific namespace services only.
**Screenshots**
<!--- If applicable, add screenshots to help explain your problem. -->

<img width="1423" height="396" alt="Image" src="https://github.com/user-attachments/assets/30b9d5bb-ff28-4d37-8559-c7a707f73c04" />

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used: 5.0.3
* Configuration: 
* Environment name and version (e.g. Kubernetes? What version?): Env: QA, EKS: 1.30 
* Server type and version: Loki 3.4.2
* Operating System and version: Linux 1.30 compatible with EKS
* Filters and plugins: Tail input with Loki output pluging

**Additional context**
<!--- How has this issue affected you? What are you trying to accomplish? --> 
- We are trying to replace promtail with fluentbit because of it's lightweight low resource usage and high performance. But blocked because of `Tenant_Id_Key tenant_id` behaviour is not working. 
- 
<!--- Providing context helps us come up with a solution that is most useful in the real world -->
NA
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4cb3476bc5cf649e9ca7df1fd22dbcbfd66920ca`.  There
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
{"case_id": "fluent_fluent_bit__11824__4cb3476",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
