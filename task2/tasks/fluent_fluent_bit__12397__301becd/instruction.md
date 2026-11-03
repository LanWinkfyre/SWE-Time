# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
OTLP/JSON: span status.code written and parsed as short enum name instead of integer

## Bug Report

**Describe the bug**

In OTLP/JSON, fluent-bit encodes and decodes the span `status.code` as a short enum
name (`UNSET` / `OK` / `ERROR`). The OTLP specification requires enum fields to be
encoded as **integers**, and the short names are not valid protobuf enum names either
(those would be `STATUS_CODE_UNSET` / `STATUS_CODE_OK` / `STATUS_CODE_ERROR`).

The result is that fluent-bit's OTLP/JSON is only interoperable with fluent-bit:

* what it **writes** is rejected by spec-compliant consumers,
* what a spec-compliant producer **writes** is rejected by fluent-bit.

We hit this while using fluent-bit as a log sink in CI: an `opentelemetry` input
receives the OTLP protobuf traffic of the machine under test and an `stdout` output
with `format: otlp_json` writes it to the journal, so the test suite can read the
telemetry back. Every span that carries a status is silently dropped by the reader,
because the OTLP/JSON unmarshaler rejects the whole record.

**To Reproduce**

Config:

```yaml
service:
  flush: 1
  log_level: info
pipeline:
  inputs:
  - name: opentelemetry
    listen: 0.0.0.0
    port: 4318
    tag: sink.traces
  outputs:
  - name: stdout
    match: sink.traces
    format: otlp_json
```

*Encoding side* - send a span with a status (OTLP/protobuf, as any SDK does) and
fluent-bit prints:

```json
{"resourceSpans":[{...,"spans":[{...,"status":{"code":"UNSET","message":""}}]}]}
{"resourceSpans":[{...,"spans":[{...,"status":{"code":"ERROR","message":"boom"}}]}]}
```

Feeding that into any pdata-based consumer (OpenTelemetry Collector
`otlpjsonfilereceiver`, `otel-tui`) drops the record without a message.

*Decoding side* - post OTLP/JSON to the same input, only the non-conformant spelling
is accepted:

```
"status":{"code":2}                    -> HTTP 400, "invalid JSON trace: conversion error (status: 43)"
"status":{"code":"STATUS_CODE_ERROR"}  -> HTTP 400, "invalid JSON trace: conversion error (status: 43)"
"status":{"code":"ERROR"}              -> HTTP 201
```

**Expected behavior**

Per
[opentelemetry-proto/docs/specification.md](https://github.com/open-telemetry/opentelemetry-proto/blob/main/docs/specification.md):

> Values of enum fields MUST be encoded as integer values. Unlike the standard
> Protobuf JSON Mapping, which allows values of enum fields to be encoded as either
> integer values or as enum name strings, only integer enum values are allowed in
> OTLP JSON Protobuf Encoding; the enum name strings MUST NOT be used.

So the encoder should write `"code": 2`, and the decoder should accept integers.

**Where in the code**

Encoder - `src/opentelemetry/flb_opentelemetry_otlp_json.c` (`create_trace_status_json`):

```c
if (status->code == CTRACE_SPAN_STATUS_CODE_OK) {
    code_string = "OK";
}
else if (status->code == CTRACE_SPAN_STATUS_CODE_ERROR) {
    code_string = "ERROR";
}
else {
    code_string = "UNSET";
}
flb_json_mut_obj_add_str(doc, json, "code", code_string);
```

Decoder - `src/opentelemetry/flb_opentelemetry_traces.c`: the `code` entry is only
read when it is a `MSGPACK_OBJECT_STR`, and only `UNSET` / `OK` / `ERROR` are mapped;
anything else returns `-1`. An integer value is not handled at all.

**Your Environment**

* Version used: 5.0.6 and 5.1.2, both reproduce (official `fluent/fluent-bit` images)
* Configuration: see above
* Environment name and version: Docker, `--network host`
* Server type and version: n/a
* Operating System and version: Linux
* Filters and plugins: `in_opentelemetry`, `out_stdout` with `format: otlp_json`

**Anything else / question before we send a PR**

We would like to fix this, but the fix is a breaking change for anyone whose pipeline
currently has fluent-bit on both ends of an OTLP/JSON hop: the encoder and the decoder
are consistent with each other today, so switching the encoder to integers without
touching the decoder would break those setups.

Our proposal would be:

1. encoder writes the integer value, as the spec requires,
2. decoder accepts integers, and keeps accepting the current short names (and
   optionally the canonical `STATUS_CODE_*` names) so existing fluent-bit to
   fluent-bit pipelines keep working.

Would you take a PR along those lines, or do you prefer the change to be gated behind
a configuration option? Happy to follow whichever direction you consider right.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `301becd3be077a946652d7d0aaeddc53c244d4ea`.  There
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
{"case_id": "fluent_fluent_bit__12397__301becd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
