# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Linux] Segfault in memory_maps() when monitored process uses hundreds of GBs of memory

## Summary

* OS: Linux
* Architecture: 64bit
* Psutil version: 5.9.0+
* Python version: 3.8+
* Type: core

## Description

If the monitored process uses hundreds of GBs of memory (for example, a large impalad process), a segfault can occur in the memory_maps() function.

Given a large enough process, the following script is sufficient to reproduce with psutil 5.9.0+ on Python 3.8, 3.10 and 3.12:
```
import psutil
import sys
pid = int(sys.argv[1])
process = psutil.Process(pid)
mm = psutil.Process.memory_maps(process)
```
Inspection of the resulting core dump with gdb shows that the backtrace contains > 65,500 calls to map_next() (this output from Python 3.10.11):
```
#0 0x0007ffb3625b6a0 in map_next (lz=0x7ffb2d7777c0) at Python/bltinmodule.c:1341
...
#65503 0x00007ffb3625b6a6 in map_next (lz=0x7ffb2c2e4be0) at Python/bltinmodule.c:1341
#65504 0x00007ffb36188bed in list_extend (iterable=<optimized out>, self=0x7ffb2c2d7500) at Objects/listobject.c:960
#65505 _PyList_Extend (self=0x7ffb2c2d7500, iterable=<optimized out>) at Objects/listobject.c:1000
...
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ed1d42549ba45f12d43792060f03eb091817efd9`.  There
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
{"case_id": "giampaolo_psutil__2496__ed1d425",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
