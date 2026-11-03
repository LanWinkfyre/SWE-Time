# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Fluent Bit crashes with dummy has flush_on_startup true and has a lua filter

## Bug Report

**Describe the bug**

Fluent Bit crashes with the following config:


```yaml

pipeline:
  inputs:
    - name: dummy
      interval_sec: 5
      flush_on_startup: true
  filters:
    - name: lua
      script: transform.lua
      call: test2
      match: "*"
  outputs:
    - name: stdout
      match: '*'
```

transform.lua
```lua
function test2(tag, timestamp, record)
    record["check"] = "checkval"
    return 2, timestamp, record
end

```

Output:

```shell
fluent-bit -c min.yml
Fluent Bit v5.0.4
* Copyright (C) 2015-2026 The Fluent Bit Authors
* Fluent Bit is a CNCF graduated project under the Fluent organization
* https://fluentbit.io

______ _                  _    ______ _ _           _____  _____ 
|  ___| |                | |   | ___ (_) |         |  ___||  _  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   _|___ \ | |/' |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / /   \ \|  /| |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V //\__/ /\ |_/ /
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/ \____(_)\___/


[2026/04/27 17:30:03.061] [ info] [fluent bit] version=5.0.4, commit=29deec9e72, pid=74078
[2026/04/27 17:30:03.062] [ info] [storage] ver=1.1.6, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2026/04/27 17:30:03.062] [ info] [simd    ] NEON
[2026/04/27 17:30:03.062] [ info] [cmetrics] version=2.1.2
[2026/04/27 17:30:03.062] [ info] [ctraces ] version=0.7.1
[2026/04/27 17:30:03.063] [ info] [input:dummy:dummy.0] initializing
[2026/04/27 17:30:03.063] [ info] [input:dummy:dummy.0] storage_strategy='memory' (memory only)
[2026/04/27 17:30:03] [engine] caught signal (SIGSEGV)
ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)ERROR: no debug info in Mach-O executable (make sure to compile with -g; may need to run dsymutil) (-1)[1]    74078 abort      $FBIT_HOME/fluent-bit -c min.yml
```


**To Reproduce**
 
- Steps to reproduce the problem:

Run with the config displayed above. It doesn't reproduce with `flush_on_startup: false`


**Expected behavior**

Do not crash.


**Your Environment**
* Version used: latest from master (`commit=29deec9e72`)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `29deec9e72a5e1ccc9996a58481bc7ba4d60353d`.  There
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
{"case_id": "fluent_fluent_bit__11751__29deec9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
