# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[linux] `Process.create_time()` changes during execution, causing mayhem.

## Summary

* OS: Ubuntu Linux 24.04
* Architecture: 64bit, ARM64
* Psutil version: 7.0.0
* Python version: 3.12
* Type: core

## Description

I've identified a significant bug when running on Linux, related to #2521, that causes the process creation time reported by `Process.create_time()` for any given process to change during execution. Because the creation time is calculated relative to the current system time, if the system time is corrected during execution (for instance due to an NTP time update, or manually), the reported creation time changes under some conditions.

Since `Process` uses the values from `create_time()` along with the PID to uniquely identify a process, this leads to very unexpected results for many methods. For instance, `Process().is_running()` can return False for the currently running process (see example below). Or where `proc.is_running()` returns False for an external process that is very much alive, but `proc.wait()` still blocks indefinitely.

## Expected behavior

Intuitively, I would expect `Process.create_time()` to return a constant value, indicating the system timestamp as recorded when the process actually started, which doesn't change if the system clock is subsequently adjusted.

## Reproducible example

This scenario is tricky to recreate, but the script below is consistently showing this error on my machine. This example attempts to change the system time during execution, so it requires `sudo` access. This can have other consequences on your system, so it might be better run in a VM or container.

```python
from datetime import datetime, timezone
import time

from psutil import boot_time, Process

print(f"Current time: {datetime.now(tz=timezone.utc)}")

boot_time_before = boot_time()
print(f"Boot time: {datetime.fromtimestamp(boot_time_before, tz=timezone.utc)}")

this_proc = Process()
create_time_before = Process().create_time()
print(f"Create time: {datetime.fromtimestamp(create_time_before, tz=timezone.utc)}")
print()

try:
    print('Changing system time by +1 hour')
    real_time = time.clock_gettime(time.CLOCK_REALTIME)
    time.clock_settime(time.CLOCK_REALTIME, real_time + 3600)
    print(f"Current time: {datetime.now(tz=timezone.utc)}")

    cached_create_time = this_proc.create_time()
    new_create_time = Process().create_time()
    print(f"Create time "
          f"cached={datetime.fromtimestamp(cached_create_time, tz=timezone.utc)}, "
          f"new={datetime.fromtimestamp(new_create_time, tz=timezone.utc)}")

    print(f"Is running: {this_proc.is_running()}")
    print()

    print('Calling psutil.boot_time()')
    boot_time_after = boot_time()
    print(f"Boot time: {datetime.fromtimestamp(boot_time_after, tz=timezone.utc)}")

    cached_create_time_after = this_proc.create_time()
    new_create_time_after = Process().create_time()
    print(f"Create time: "
          f"cached={datetime.fromtimestamp(cached_create_time_after, tz=timezone.utc)}, "
          f"new={datetime.fromtimestamp(new_create_time_after, tz=timezone.utc)}")

    print(f"Is running: {this_proc.is_running()}")
    print(f"this_proc == Process(): {this_proc == Process()}")
finally:
    time.clock_settime(time.CLOCK_REALTIME, real_time)
```

## Results

The output of the above script is reproduced below:

```
Current time: 2025-03-21 01:18:56.465400+00:00
Boot time: 2025-03-06 18:06:38+00:00
Create time: 2025-03-21 01:18:55.630000+00:00

Changing system time by +1 hour
Current time: 2025-03-21 02:18:56.465695+00:00
Create time cached=2025-03-21 01:18:55.630000+00:00, new=2025-03-21 01:18:55.630000+00:00
Is running: True

Calling psutil.boot_time()
Boot time: 2025-03-06 19:06:38+00:00
Create time: cached=2025-03-21 01:18:55.630000+00:00, new=2025-03-21 02:18:55.630000+00:00
Is running: False
this_proc == Process(): False

```

## Cause

I've traced the cause as best I can, but there is not a good workaround to avoid the issue.

On linux, `Process.create_time` calculates the process creation time by adding the unix `btime` timestamp from `/proc/stat` to the process starttime from `/proc/<pid>/stat`, which records the system counter time elapsed since startup.

The `btime` value in `/proc/stat` also changes when the system time is updated, and appears to report the current unix timestamp minus the system uptime, rather than the actual system HW time at startup.

However, the `btime` value is cached in `psutil._pslinux.BOOT_TIME` every time `psutil._pslinux.boot_time()` is called, and this cached value is used to calculate `Process.create_time()`, which is also cached. So if the system time changes and the cached values are recalculated (due to explicitly calling `psutil.boot_time()` or creating a new `Process()` instance), different values are returned for `boot_time()` or `create_time()`.

## Partial solution

Because process PID and create_time are used to uniquely identify each running process, it is essential that this identifier remains unique and constant for any given process under any circumstances. Because the linux `btime` value is not actually a constant, it would seem more reliable to use the monotonic counter `starttime` recorded in `/proc/<pid>/stat` together with the PID to uniquely identify each process in `Process._ident`, since the `starttime` value does not change.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `65ef1d0f8f08c992b3c7259c424cf36269955ed7`.  There
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
{"case_id": "giampaolo_psutil__2526__65ef1d0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
