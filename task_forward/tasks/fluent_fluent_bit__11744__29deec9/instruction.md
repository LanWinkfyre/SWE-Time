# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
engine: shutdown hangs at 100% CPU when duplicate STOP signals arrive

## Bug Report

**Describe the bug**
While testing the `in_tail` input plugin with `exit_on_eof on`, I sent a `kill` (SIGTERM) to terminate the Fluent Bit process during the test.
The process did not exit: the pipeline thread pinned one CPU core at 100% and no further log lines were emitted.
The grace period elapsed but the service never reached the "service has stopped" state. 

**To Reproduce**
- Rubular link if applicable:
- Example log message if applicable:
```
[2026/04/21 15:10:43.361] [ warn] [engine] service will shutdown in max 600 seconds
[2026/04/21 15:10:43.361] [ info] [engine] pausing all inputs..
...
[2026/04/21 15:10:44.065] [ warn] [engine] service will shutdown in max 600 seconds
[2026/04/21 15:10:44.065] [ info] [engine] pausing all inputs..
[2026/04/21 15:10:44.065] [ info] [input] pausing storage_backlog.1
```
- Steps to reproduce the problem:

1. Configure `in_tail` with an exit_on_eof path. 
2. When the input reaches its termination condition it calls `flb_engine_exit()` internally (first STOP, exit_on_eof). 
3. Within a short window, send an external `SIGTERM` (second STOP via `flb_stop()` → `flb_engine_exit()`). 
4. The engine busy-loops and never exits within the grace period.

**Expected behavior**
Any number of STOP signals should be idempotent. The engine should complete shutdown within the configured grace period and exit cleanly (exit code from `exit_status_code`).

**Screenshots**
<!--- If applicable, add screenshots to help explain your problem. -->

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used: 5.0.3
* Configuration: 
```
[SERVICE]
    flush 1
    grace 60
    log_level info
    log_file /tmp/testing/logs/testing.log
    parsers_file /tmp/testing/parsers.conf
    plugins_file /tmp/testing/plugins.conf
    http_server on
    http_listen 0.0.0.0
    http_port 22002

    storage.path /tmp/testing/storage
    storage.metrics on
    storage.max_chunks_up 512
    storage.sync full
    storage.checksum off
    storage.backlog.mem_limit 100M

[INPUT]
    Name tail
    Path /tmp/testing.input
    Exclude_Path *.gz,*.zip
    Tag testing
    Key message
    Offset_Key   log_offset

    Read_from_Head true
    Refresh_Interval 3
    Rotate_Wait 31557600

    Buffer_Chunk_Size 1MB
    Buffer_Max_Size 16MB
    Inotify_Watcher false

    storage.type filesystem
    storage.pause_on_chunks_overlimit true

    DB /tmp/testing/storage/testing.db
    DB.sync normal
    DB.locking false

    exit_on_eof on

    Alias input_log

[OUTPUT]
    Name file
    Match *
    File /tmp/testing.out
```
* Environment name and version: bare-metal
* Server type and version: x86_64
* Operating System and version: RHEL 8.10 (kernel 4.18) and Ubuntu 22.04 (kernel 6.8) — both affected 
* Filters and plugins: `in_tail` also reproducible with minimal `in_lib` + `out_null` 

**Additional context**
From my analysis, the issue appears to be triggered by the second STOP re-entering the handler block in `flb_engine_start()`, which resets `config->event_shutdown->status` to `MK_EVENT_NONE` even though the shutdown timerfd is still registered in the kernel's epoll set.
The dispatcher would then likely drop the timer event (via the `status != MK_EVENT_NONE` guard in `flb_event_load_bucket_queue()`), while the level-triggered timerfd keeps reporting EPOLLIN — which would explain the infinite busy-loop in the pipeline thread and why `grace_count` never advances, leaving `flb_engine_shutdown()` unreachable.
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
{"case_id": "fluent_fluent_bit__11744__29deec9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
