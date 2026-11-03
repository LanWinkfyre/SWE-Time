# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_forward: only the first cmetrics context per metrics payload is ingested (silent metric loss)

## Bug Report

**Describe the bug**

`in_forward` ingests only the **first** cmetrics context in a metrics
payload and silently discards the remainder of the buffer.

`out_forward`'s `flush_forward_mode()` sends metric events as
`[tag, bin(raw cmetrics msgpack), options{fluent_signal: METRICS}]` —
the entire chunk goes on the wire as a single BIN payload. A chunk
routinely holds several cmetrics contexts. The receiver calls
`cmt_decode_msgpack_create()` once and ignores everything past the first
context.

Nothing reports the loss:

- no error is logged
- the flush returns success
- record-level counters do not track metric events, so
  `fluentbit_input_records_total`,
  `fluentbit_output_dropped_records_total`,
  `fluentbit_output_retries_failed_total` and
  `fluentbit_output_proc_records_total` all remain at zero while data
  disappears

In our production pipeline this cost roughly **40% of metric samples**
over the forward hop, undetected, because no counter or log line can
observe it.

`plugins/in_forward/fw_prot.c`, metrics branch of `append_log()`:

```c
ret = cmt_decode_msgpack_create(&cmt, (char *) data, len, &off);
if (ret != CMT_DECODE_MSGPACK_SUCCESS) {
    flb_plg_error(ins, "cmt_decode_msgpack_create failed. ret=%d", ret);
    return -1;
}
/* single ingest — the rest of the buffer past `off` is dropped */
```

For contrast, `out_prometheus_remote_write` handles the same structure
correctly in `cb_prom_flush()`:

```c
while ((ret = cmt_decode_msgpack_create(&cmt, (char *) event_chunk->data,
                                        event_chunk->size, &off)) == ok) {
    ...
}
```

**To Reproduce**

Two `prometheus_scrape` inputs sharing one tag guarantee multiple
cmetrics contexts in a single chunk; a `Flush` longer than the scrape
interval guarantees they are batched into one forward payload.

1. Two trivial exporters — `exp.py`:

```python
#!/usr/bin/env python3
import http.server, socketserver, sys

name, port = sys.argv[1], int(sys.argv[2])
body = ('# HELP %s test\n# TYPE %s counter\n%s{src="%s"} 1\n'
        % (name, name, name, name)).encode()

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(('127.0.0.1', port), H).serve_forever()
```

```bash
python3 exp.py metric_a 9101 &
python3 exp.py metric_b 9102 &
```

2. `receiver.conf`:

```ini
[SERVICE]
    Flush     1
    Log_Level info
    Daemon    Off

[INPUT]
    Name      forward
    Listen    127.0.0.1
    Port      24334
    Tag       metrics

[OUTPUT]
    Name      stdout
    Match     metrics
```

3. `sender.conf`:

```ini
[SERVICE]
    Flush     5
    Log_Level info
    Daemon    Off

[INPUT]
    Name             prometheus_scrape
    Host             127.0.0.1
    Port             9101
    Tag              metrics
    Scrape_Interval  2

[INPUT]
    Name             prometheus_scrape
    Host             127.0.0.1
    Port             9102
    Tag              metrics
    Scrape_Interval  2

[OUTPUT]
    Name             forward
    Match            metrics
    Host             127.0.0.1
    Port             24334
```

4. Run both and count:

```bash
fluent-bit -c receiver.conf > recv.log 2>&1 &
fluent-bit -c sender.conf   > send.log  2>&1 &
sleep 30

grep -c metric_a recv.log
grep -c metric_b recv.log
```

**Expected behavior**

Both `metric_a` and `metric_b` appear on the receiver — the chunk
contains a cmetrics context for each scrape input, and both should be
ingested.

**Actual behavior**

Only one of the two ever appears. The second context sits past `off` in
the same BIN payload and is discarded with no error.

Instrumenting the decode to report how much of the buffer was consumed
makes it explicit:

```c
flb_plg_debug(ins, "decoded: off=%zu len=%zu remaining=%zu",
              off, len, (size_t) (len - off));
```

Production traffic, five-minute window — **91 of ~120 metrics payloads
carried unconsumed data**:

```
decoded: off=34640   len=347843   remaining=313203   (90% discarded)
decoded: off=263368  len=2135781  remaining=1872413  (88% discarded)
decoded: off=302957  len=2158795  remaining=1855838  (86% discarded)
decoded: off=366010  len=2177213  remaining=1811203  (83% discarded)
decoded: off=525075  len=1573207  remaining=1048132  (67% discarded)
decoded: off=367770  len=728136   remaining=360366   (49% discarded)
```

**Quantified end-to-end impact**

The same upstream series were delivered simultaneously over
`prometheus_remote_write` and over `forward`, from a single Fluent Bit
process, into two separate VictoriaMetrics instances — one control path,
one test path.

```promql
avg(count_over_time(container_http_server_requests_total[5m]))
```

| ingest path | before | after a local fix |
| --- | --- | --- |
| `prometheus_remote_write` (control) | — | — |
| `forward` | **77%** of control | **100.0 – 100.2%** of control |

Byte-level parity between the two outputs, taken from a single
synchronised scrape (no timing skew):

| output | delta over 60s |
| --- | --- |
| remote_write path | 1,375,153,673 |
| forward path | 1,297,363,468 |

**54% → 94.3%** by bytes. The residual is attributable to the two paths
carrying traffic from a different mix of senders, not to this defect.

**Your Environment**

- Version used: **4.0.4** (receiver) and **4.0.8** (sender). The same
  single-call pattern is present in **5.1.0** and on **master**.
- Configuration: see reproduction above
- Environment name and version: Kubernetes (GKE) sender → Docker
  receiver
- Server type and version: linux/amd64
- Operating System and version: Debian (official container images)
- Filters and plugins: `prometheus_remote_write` (in),
  `prometheus_scrape` (in), `forward` (in/out), `opentelemetry` (out)

**Additional context**

A great deal of metric data can be lost with no observable signal. In our
case roughly 40% of samples over the forward hop, for an extended period,
while every drop counter read zero.

Two related observations found while diagnosing this:

1. **`out_file` has the identical defect.** `print_metrics_text()` in
   `plugins/out_file/file.c` calls `cmt_decode_msgpack_create()` once
   with no loop, and `cb_file_flush()` returns `FLB_OK` unconditionally
   for metric chunks. A metrics file therefore contains only the first
   context of each chunk. This makes `out_file` unusable for verifying
   metric pipelines — it misled our own investigation for some time. The
   symptom was previously reported in #11018 (closed as not planned, no
   root cause identified). Happy to open this separately if preferred.

2. **Metric events are invisible to the record counters.** This is what
   allowed the bug to persist undetected. `proc_bytes_total` is currently
   the only telemetry that tracks metric traffic. Possibly worth
   documenting even if the behaviour is intentional.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a51fc600d8e7f460dc72bd5464458b7798d2fb2c`.  There
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
{"case_id": "fluent_fluent_bit__12373__a51fc60",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
