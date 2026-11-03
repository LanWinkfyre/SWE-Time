# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_storage_backlog: persisted chunk without a matching route blocks hot reload

## Bug

`in_storage_backlog` registers a persisted filesystem chunk even when its tag matches no output, but it does not add the chunk to an output backlog queue. ChunkIO continues to count the chunk even though nothing can dispatch it.

During thread-safe hot reload, Fluent Bit sets the old context's shutdown grace to `-1`. The old engine then waits indefinitely for the filesystem chunk count to reach zero. The replacement context cannot start, and the hot-reload watchdog eventually aborts the process.

## Reproduction

Using a Linux build from current `master`, seed a filesystem chunk:

```ini
# /tmp/seed.conf
[SERVICE]
    Flush        1
    storage.path /tmp/flb-no-route-storage

[INPUT]
    Name         dummy
    Tag          stale
    Samples      1
    storage.type filesystem

[OUTPUT]
    Name         http
    Match        stale
    Host         127.0.0.1
    Port         9
    Retry_Limit  no_limits
```

Restart with no output matching `stale`, then hot reload:

```ini
# /tmp/reload.conf
[SERVICE]
    Flush               1
    Hot_Reload          On
    Hot_Reload.Timeout  3
    storage.path        /tmp/flb-no-route-storage

[INPUT]
    Name         tail
    Tag          live
    Path         /tmp/no-such-file
    storage.type filesystem

[OUTPUT]
    Name   null
    Match  live
```

```sh
mkdir /tmp/flb-no-route-storage

# Send SIGKILL after two seconds, leaving the filesystem chunk on disk.
timeout -s KILL 2 fluent-bit -c /tmp/seed.conf >/tmp/seed.log 2>&1

# Send SIGHUP after two seconds and let the hot-reload watchdog abort the process.
timeout -s HUP 2 fluent-bit -c /tmp/reload.conf
```

## Observed behavior

At startup, storage backlog reports that it registered the old chunk. It never reports that it queued the chunk:

```text
[input:storage_backlog:storage_backlog.1] register dummy.0/7-1785875360.662289377.flb
```

SIGHUP then leaves the old engine waiting on that one filesystem chunk until the watchdog aborts:

```text
[engine] caught signal (SIGHUP)
[reload] stop everything of the old context
[engine] service will shutdown when all remaining tasks are flushed
[engine] pausing all inputs..
[engine] pending chunk count: memory=0, filesystem=1; grace_timer=1
[engine] pending chunk count: memory=0, filesystem=1; grace_timer=2
[engine] pending chunk count: memory=0, filesystem=1; grace_timer=3
[engine] pending chunk count: memory=0, filesystem=1; grace_timer=4
[hot_reload_watchdog] Hot reload timeout exceeded (3 seconds), aborting to prevent indefinite hang
```

The replacement context never reaches `[reload] start everything`.

## Cause

`sb_append_chunk_to_segregated_backlogs()` computes the restored chunk's routes but ignores the return value from `flb_routes_mask_set_by_tag()`:

```c
flb_routes_mask_set_by_tag(dummy_input_chunk.routes_mask, tag_buf, tag_len,
                           context->ins);
```

When no output matches, the loop adds no backlog queue entry, yet the function still returns success:

```c
mk_list_foreach_safe(head, tmp, &context->backlogs) {
    backlog = mk_list_entry(head, struct sb_out_queue, _head);
    if (flb_routes_mask_get_bit(dummy_input_chunk.routes_mask,
                                backlog->ins->id,
                                backlog->ins->config->router)) {
        result = sb_append_chunk_to_segregated_backlog(target_chunk, stream,
                                                       chunk_size, backlog);
        if (result) {
            return -3;
        }
    }
}

return 0;
```

`sb_segregate_chunks()` treats that result as a successful registration, locks the chunk, and moves it down:

```c
ret = sb_append_chunk_to_segregated_backlogs(chunk, stream, context);
if (ret) {
    /* error handling */
    continue;
}

flb_plg_info(context->ins, "register %s/%s", stream->name, chunk->name);
cio_chunk_lock(chunk);
cio_chunk_down(chunk);
```

Because no `sb_out_queue` contains the chunk, `cb_queue_chunks()` can never map it back into an input chunk or create an output task. `flb_engine_flush()` therefore cannot process it, while ChunkIO continues to include it in `chunks_fs`.

Thread-safe hot reload prevents the old context from escaping this state:

```c
if (old_config->ensure_thread_safety_on_hot_reloading) {
    old_config->grace = -1;
}
```

With `grace == -1`, `chunks_fs=1` prevents `flb_engine_shutdown()` from running, so storage is never destroyed. `flb_reload()` remains blocked in `flb_stop(old_ctx)` and cannot start the new context.

## Expected behavior

A persisted chunk with no route in the current configuration should remain on disk without being counted as work the old context can drain. The replacement context should reopen and reconsider the chunk because its configuration may restore the route. Deleting the chunk merely to unblock shutdown would turn a temporary routing change into silent data loss.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fe293d4270b27bc078e0bb82e7aa2afe08e723f8`.  There
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
{"case_id": "fluent_fluent_bit__12225__fe293d4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
