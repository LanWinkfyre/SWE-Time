# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
log: out-of-bounds stack read in `flb_log_suppress_check()` for log messages larger than 4096 bytes

## Bug Report

**Describe the bug**

`flb_log_suppress_check()` (`include/fluent-bit/flb_log.h`) formats the message into a 4096-byte stack buffer and passes the `vsnprintf()` return value as the length:

```c
char buf[4096];
...
size = vsnprintf(buf, sizeof(buf) - 1, fmt, args);
...
ret = flb_log_cache_check_suppress(w->log_cache, buf, size);
```

`vsnprintf()` returns the length the message *would* have had, so for a longer message `buf` is truncated but `size` is not. `flb_log_cache_check_suppress()` then copies `size` bytes out of that buffer (`flb_sds_copy()` → `memcpy()` in `src/flb_log.c:722`), reading past the end of the stack frame and caching the out-of-bounds bytes.

Any plugin instance with `log_suppress_interval` > 0 can hit this; plugins that log an HTTP response payload (for example `in_kubernetes_events`, `out_es`, `out_azure_kusto`, `out_cloudwatch_logs`) do so with remote-controlled data.

Seen on master (5.1.1, `48e36fcc7`); the code is unchanged since `ff5e07d` (2023-04-13). Open PR #12325 touches the same function but not this part.

**To Reproduce**

```sh
cmake -S . -B build -DSANITIZE_ADDRESS=On -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build -j
./build/bin/fluent-bit -c repro.conf
```

`repro.conf`:

```ini
[SERVICE]
    flush     1
    log_level info

[INPUT]
    name      dummy
    rate      1

[FILTER]
    name                  lua
    match                 *
    code                  function cb(tag, ts, record) error(string.rep("A", 8192)) end
    call                  cb
    log_suppress_interval 10s

[OUTPUT]
    name      null
    match     *
```

The first record makes `filter_lua` log the 8 KiB Lua error, and ASan aborts:

```text
==22796==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x00016b06b5e0
READ of size 8234 at 0x00016b06b5e0 thread T1
    #1 flb_sds_copy flb_sds.c:274
    #2 flb_log_cache_check_suppress flb_log.c:722
    #3 flb_log_suppress_check flb_log.h:223
    #4 cb_lua_filter lua.c:579
    ...
Address 0x00016b06b5e0 is located in stack of thread T1 at offset 4160 in frame
    #0 flb_log_suppress_check flb_log.h:199
  This frame has 2 object(s):
    [32, 40) 'args' (line 202)
    [64, 4160) 'buf' (line 203) <== Memory access at offset 4160 overflows this variable
```

**Expected behavior**

The suppression check uses only the bytes actually written to `buf`, truncating oversized messages instead of reading past the buffer.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `37c279fc47f41c2e069163186d660e9998900b64`.  There
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
{"case_id": "fluent_fluent_bit__12342__37c279f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
