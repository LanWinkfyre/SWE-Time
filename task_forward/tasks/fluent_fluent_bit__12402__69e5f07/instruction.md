# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
storage: misleading "cannot mmap/read chunk" error flood when max_chunks_up is saturated

## Bug Report

**Describe the bug**

When an output is slower than the inputs (plain backpressure, no network errors), the log fills with `[error] [storage] cannot mmap/read chunk` lines, even though there is no real mmap failure and no data problem. The errors fire once per chunk creation while the `storage.max_chunks_up` quota is saturated, so a healthy pipeline under backpressure logs hundreds of ERROR lines per minute. This breaks log-based alerting and makes users troubleshoot the wrong problem (we initially suspected memory/mmap exhaustion).

What happens: with the output being slow, in-flight tasks keep their chunks up until the `storage.max_chunks_up` quota is fully used. From that point on, every new chunk created by an input with `storage.type filesystem` is born *down*, as expected ([`open_and_up()`, `cio_file.c:566`](https://github.com/fluent/fluent-bit/blob/v5.1.1/lib/chunkio/src/cio_file.c#L566), early return at [`cio_file.c:705`](https://github.com/fluent/fluent-bit/blob/v5.1.1/lib/chunkio/src/cio_file.c#L705)).
Right after `flb_input_chunk_create()` returns the new chunk in down state (it is brought up to write the header and set down again, [`flb_input_chunk.c:2482-2546`](https://github.com/fluent/fluent-bit/blob/v5.1.1/src/flb_input_chunk.c#L2482)), `flb_input_chunk_get_projected_write_size()` calls [`cio_meta_size()` at `flb_input_chunk.c:995`](https://github.com/fluent/fluent-bit/blob/v5.1.1/src/flb_input_chunk.c#L995) on that down chunk. The call fails before any mmap happens — `cio_file_native_map()` returns early because the fd is closed ([`cio_file_unix.c:82`](https://github.com/fluent/fluent-bit/blob/v5.1.1/lib/chunkio/src/cio_file_unix.c#L82)) —
but `mmap_file()` still logs the error ([`cio_file.c:424`](https://github.com/fluent/fluent-bit/blob/v5.1.1/lib/chunkio/src/cio_file.c#L424)).

There is a second problem: on that failure, `get_projected_write_size()` returns `SIZE_MAX` ([`flb_input_chunk.c:995-999`](https://github.com/fluent/fluent-bit/blob/v5.1.1/src/flb_input_chunk.c#L995)), and that value goes into `flb_input_chunk_has_overlimit_routes()`, where `fs_chunks_size + fs_backlog_chunks_size + SIZE_MAX` overflows `size_t` ([`flb_input_chunk.c:1226`](https://github.com/fluent/fluent-bit/blob/v5.1.1/src/flb_input_chunk.c#L1226)).
The result depends on the queue size:

| Queue vs `storage.total_limit_size` | What happens |
|---|---|
| Below the cap | The wraparound masks the value; the chunk is placed normally. Only the error flood is visible. |
| At the cap | The overlimit check turns true and `find_space_new_data(ic, SIZE_MAX)` tries to free an impossible amount of space: it strips routes from queued chunks (discarding buffered data), `place_new_chunk()` returns 0, the new chunk is destroyed and the incoming records are dropped (`[input chunk] no available chunk`). |

The same code path is present on current `master`.

**To Reproduce**

Use the following config. The sink is [calyptia-https-benchmark-server](https://github.com/chronosphereio/calyptia-https-benchmark-server) with `-delayseconds=2`: it returns 200 to every request but serves ~1 request every 2 seconds (slow downstream, no errors). Compose builds it straight from the GitHub repo. `max_chunks_up` is set low only to reach saturation in seconds; the same happens with the default once enough tasks are in flight.

fluent-bit.yml

```yaml
service:
  flush: 1
  log_level: info
  storage.path: /fb-storage/
  storage.max_chunks_up: 8

pipeline:
  inputs:
    - name: dummy
      rate: 500
      storage.type: filesystem
    - name: dummy
      rate: 500
      storage.type: filesystem
    - name: dummy
      rate: 500
      storage.type: filesystem
  outputs:
    - name: http
      match: '*'
      host: sink
      port: 8443
      format: json_lines
      tls: on
      tls.verify: off
```

compose.yml

```yaml
services:
  sink:
    build:
      context: https://github.com/chronosphereio/calyptia-https-benchmark-server.git
    command: ["./https-benchmark-server", "-delayseconds=2", "-printrecords=false"]
  fluent-bit:
    image: fluent/fluent-bit:5.1.1
    command: ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fb.yml"]
    volumes: ["./fluent-bit.yml:/fluent-bit/etc/fb.yml:ro"]
    depends_on: [sink]
```

- Steps to reproduce the problem:

Run the stack and wait one minute.

```shell
docker compose -f compose.yml up -d --build
sleep 60
docker compose -f compose.yml logs fluent-bit | grep -c "cannot mmap"
```

We can see ~40 errors in the first 60 seconds, and the count keeps growing:

```text
[2026/09/11 19:25:19.037] [error] [storage] cannot mmap/read chunk '/fb-storage//dummy.0/1-1789154719.37848216.flb'
[2026/09/11 19:25:21.038] [error] [storage] cannot mmap/read chunk '/fb-storage//dummy.0/1-1789154721.37827717.flb'
```

We can also see that:

- The failing chunk name always matches the log line timestamp to the millisecond (chunk names are `PID-secs.nanos.flb`, generated at creation), so the failure happens inside the creation call stack.
- There are zero `errno=` lines on stderr (chunkio prints the OS error for any real mmap/fstat failure) and zero companion messages (`[cio file] cannot map chunk`, `[input chunk] could not create chunk file`).
  This rules out the other emitter paths and confirms the fd-closed early return.
- With `http_server on`, `watch -n 1 'curl http://localhost:2020/api/v2/metrics | grep -i chunks'` shows `fs_chunks_up` pinned at `storage.max_chunks_up`, all busy with tasks.

**Expected behavior**

To not log ERROR entries for a state that is part of normal `max_chunks_up` operation: getting the projected size of a chunk the engine itself just set down should not require mapping it. Also:

- A failed metadata read should not become `SIZE_MAX` inside the `total_limit_size` accounting; the arithmetic in `has_overlimit_routes()`/`find_space_new_data()` should be overflow-safe.
- `cannot mmap/read chunk` should be reserved for real mmap/read failures (with errno); "chunk is down / fd not open" is a different, expected condition.

**Screenshots**

N/A (log output above).

**Your Environment**

* Version used: v5.1.1 (docker image `fluent/fluent-bit:5.1.1`; also observed on a production Linux deployment of v5.1.1). Same code path on `master`.
* Configuration: see above (filesystem storage inputs + single slow output)
* Environment name and version: Docker Compose (repro); systemd service on Linux (original report)
* Server type and version: any — reproduced with a plain HTTP(S) sink
* Operating System and version: repro on Docker (Linux containers); original on OSX
* Filters and plugins: in_dummy/in_tail with `storage.type filesystem`, out_http/out_forward — the problem is output-agnostic

**Additional context**

We first saw this on a production host running 16 tail inputs (syslog trees) with filesystem storage into a single forward output with a slow receiver: a SIGCONT dump showed 255/256 chunks up, ~254 tasks running against the output, a growing on-disk queue and a sustained flood of `cannot mmap/read chunk` (~5/s). The error rate matches the chunk creation rate 1:1 while `fs_chunks_up == max_chunks_up`.

Workaround: partial only. We tested the same repro with `storage.pause_on_chunks_overlimit on` in all the inputs: the errors drop but do not stop (14 in 90 s vs ~60 without the option), because the inputs oscillate around the quota (52 `paused (storage buf overlimit 8/8)` / 49 `resume (storage buf overlimit 7/8)` messages in the same 90 s) and every chunk created right at the boundary still hits the error; it keeps memory under control, tho. At least for the loads I tried. It also changes the semantics: ingestion becomes coupled to the output speed, which is what filesystem buffering is meant to avoid, and for network inputs pausing means dropping data at the socket. Raising `storage.max_chunks_up` reduces the frequency at the cost of memory; fixing the slow downstream ("-delayseconds=0") removes the condition.

Some ideas for the fix — I could work on PRs for both:

1. fluent-bit, `flb_input_chunk_get_projected_write_size()`:
   - avoid the chunkio metadata read: Fluent Bit writes the chunk metadata itself (`input_chunk_write_header()`), so its size can be cached in `struct flb_input_chunk` at write time; or fall back to the down-safe `cio_chunk_get_real_size()` (fs_size/stat) when the chunk is down, which is also consistent with the `fs_chunks_size` accounting (based on real sizes);
   - never return `SIZE_MAX`: propagate the error and skip the placement enforcement for that append;
   - make the arithmetic in `has_overlimit_routes()`/`find_space_new_data()` overflow-safe and reject `chunk_size > total_limit_size` explicitly.
2. chunkio: distinguish "file not open" from a real mmap failure in `cio_file_native_map()`/`mmap_file()`: keep the ERROR (with errno) for syscall failures, and return a distinct status / log at debug for the fd-closed case. Other callers (`cio_chunk_get_content`, `cio_meta_read`/`cmp` via `cio_file_read_prepare`) can also land on a down chunk. The metadata length is at fixed offsets 22-23 of the 24-byte file header (`cio_file_st.h`), so a down-safe `cio_meta_size()` using `pread` is another option.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `69e5f07bb5ac8bdac6f248a47df995201f2fe851`.  There
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
{"case_id": "fluent_fluent_bit__12402__69e5f07",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
