# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
azure_logs_ingestion plugin causes Fluent Bit to segfault during --dry-run

## Bug Report
Using the `azure_logs_ingestion` output plugin causes Fluent Bit to crash with a segmentation fault when running with `--dry-run`.

This reproduces with the latest Fluent Bit container image and a minimal configuration. If the `azure_logs_ingestion` output is removed from the config, `--dry-run` completes successfully.

**To Reproduce**
- Save the **azure_logs_ingestion** documentation example config as a file with name: _fluent_bit.yaml_. Content taken from the documentation page ([azure_logs_ingestion docs](https://docs.fluentbit.io/manual/data-pipeline/outputs/azure_logs_ingestion)):

```
pipeline:
  inputs:
    - name: tail
      path: /path/to/your/sample.log
      tag: sample
      key: RawData

    # Or use other plugins
    #- name: cpu
    #  tag: sample

  filters:
    - name: modify
      match: sample
      # Add a json key named "Application":"fb_log"
      add: Application fb_log

  outputs:
    # Enable this section to see your json-log format
    #- name: stdout
    #  match: '*'

    - name: azure_logs_ingestion
      match: sample
      client_id: XXXXXXXX-xxxx-yyyy-zzzz-xxxxyyyyzzzzxyzz
      client_secret: some.secret.xxxzzz
      tenant_id: XXXXXXXX-xxxx-yyyy-zzzz-xxxxyyyyzzzzxyzz
      dce_url: https://log-analytics-dce-XXXX.region-code.ingest.monitor.azure.com
      dcr_id: dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      table_name: ladcr_CL
      time_generated: true
      time_key: Time
      compress: true
```

- Run the container with --dry-run command: 
 `docker run -ti -v ./fluent-bit.yaml:/fluent-bit/etc/fluent-bit.yaml \
  cr.fluentbit.io/fluent/fluent-bit \
  -c /fluent-bit/etc/fluent-bit.yaml`

- Result of the run command:
 Fluent Bit crashes with SIGSEGV, with the trace pointing to output shutdown:

```
PS C:\Source> docker run -ti -v ./fluent-bit.yaml:/fluent-bit/etc/fluent-bit.yaml cr.fluentbit.io/fluent/fluent-bit -c /fluent-bit/etc/fluent-bit.yaml --dry-run
Fluent Bit v5.0.5
* Copyright (C) 2015-2026 The Fluent Bit Authors
* Fluent Bit is a CNCF graduated project under the Fluent organization
* https://fluentbit.io

______ _                  _    ______ _ _           _____  _____ 
|  ___| |                | |   | ___ (_) |         |  ___||  _  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   _|___ \ | |/' |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / /   \ \|  /| |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V //\__/ /\ |_/ /
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/ \____(_)\___/


[2026/05/08 09:09:53] [engine] caught signal (SIGSEGV)
#0  0x647f64480f54      in  flb_output_exit() at src/flb_output.c:587
#1  0x647f64495b84      in  flb_engine_shutdown() at src/flb_engine.c:1356
#2  0x647f64463ae4      in  flb_destroy() at src/flb_lib.c:246
#3  0x647f643cf758      in  flb_main_run() at src/fluent-bit.c:1445
#4  0x7b988a730ca7      in  ???() at ???:0
#5  0x7b988a730d64      in  ???() at ???:0
#6  0x647f643cd170      in  ???() at ???:0
#7  0xffffffffffffffff  in  ???() at ???:0
```

**Expected behavior**
--dry-run should validate the configuration and exit cleanly without crashing.

**Screenshots**

<img width="1676" height="533" alt="Image" src="https://github.com/user-attachments/assets/97d35ac5-64ef-432c-8c48-2450ea67a633" />

**Your Environment**
* Version used: **3.1.7-5.0.5**
* Configuration: **Minimal example configuration from plugin docs page: ([azure_logs_ingestion docs](https://docs.fluentbit.io/manual/data-pipeline/outputs/azure_logs_ingestion))**
* Environment name and version: **Tested with same result on Oracle Linux and Windows Docker Desktop with WSL 2**
* Operating System and version: **Oracle Linux, WSL 2**
* Filters and plugins: **azure_logs_ingestion**

**Additional context**
The issue prevents me from validating configuration using --dry-run prior to release.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `811b5ef3a4f2167d4387969d7486dc96bf87e2ad`.  There
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
{"case_id": "fluent_fluent_bit__11789__811b5ef",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
