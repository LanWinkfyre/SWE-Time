# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_exec: long-running command blocks threaded input shutdown during hot reload

## Bug

A threaded `exec` input cannot stop during hot reload if its command keeps stdout open.

The collector remains inside `fgets()` until the child closes stdout. During reload, Fluent Bit signals the input thread to exit and then waits for it with `pthread_join()`. The input thread cannot process that exit event until the collector callback returns.

Reload hangs until the hot-reload watchdog aborts Fluent Bit. The child remains alive after the abort.

## Reproduction

Use `/tmp/flb-exec-repro.conf`:

```ini
[SERVICE]
    Flush               1
    Log_Level           debug
    Hot_Reload          On
    Hot_Reload.Timeout  3

[INPUT]
    Name          exec
    Alias         source.exec
    Command       tail -f /dev/null
    Interval_Sec  1
    Threaded      On
    Tag           exec

[OUTPUT]
    Name   null
    Match  *
```

The three-second timeout shortens the reproduction; the hang otherwise lasts until the configured watchdog timeout.

```sh
fluent-bit -c /tmp/flb-exec-repro.conf &
pid=$!
sleep 2
kill -HUP "$pid"
```

## Actual behavior

Fluent Bit begins stopping the old context, stops the output worker, and makes no further reload progress. The watchdog then aborts it:

```text
[engine] caught signal (SIGHUP)
[reload] stop everything of the old context
[output:null:null.0] thread worker #0 stopping...
[output:null:null.0] thread worker #0 stopped
[hot_reload_watchdog] Hot reload timeout exceeded (3 seconds), aborting to prevent indefinite hang
```

After 3.167 seconds, Fluent Bit exits with status 134 while the child remains alive:

```text
reload_to_exit_seconds=3.167
Fluent Bit exit status: 134
exec child is still alive
```

Status 134 is the watchdog's `SIGABRT`.

While reload is stuck, the main thread waits for the input thread:

```text
flb_reload
  flb_destroy
    flb_engine_shutdown
      flb_input_exit_all
        flb_input_instance_exit
          flb_input_thread_instance_exit
            pthread_join
```

At the same time, the threaded exec worker blocks reading the child pipe:

```text
input_thread
  input_collector_fd
    in_exec_collect
      fgets
        read
```

The main thread waits for the input thread, which cannot process its exit event until the collector returns. The collector cannot return until the child closes stdout, but Fluent Bit never stops the child.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cbe12539d4fab7e332463abac75836f82ce46a39`.  There
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
{"case_id": "fluent_fluent_bit__12185__cbe1253",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
