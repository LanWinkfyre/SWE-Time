# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
OTEL trace_id and span_id are malformed

## Bug Report

**Describe the bug**
TraceId and SpanId are malformed and unrecoverable after processing by fluent-bit. 

**To Reproduce**
- Send example log with valid trace_id and span_id:
```{"resourceLogs":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}}]},"scopeLogs":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"somescopeattribute"}}]},"logRecords":[{"timeUnixNano":"1774877764000000000","observedTimeUnixNano":"1774877764000000000","severityNumber":2,"severityText":"INFO","traceId":"c413d5b5fea3657325ff663320c7fd10","spanId":"77651bbd5ce0ce99","body":{"kvlistValue":{"values":[{"key":"specversion","value":{"stringValue":"1.0"}},{"key":"id","value":{"stringValue":"3c344379-2eee-404b-b144-79ffbee05861"}}]}}}]}]}]}```
- Watch fluent-bit's application logs
- Download file uploaded to i.e. S3 output 

**Expected behavior**
In files uploaded to S3 output trace_id and span_id are the same as sent to fluent-bit.

**Data**
- Application logs:
```
[0] [ info] [stdout] [1774869525.18446744071602915947, {"otlp"=>{"observed_timestamp"=>1774869525066000000, "severity_number"=>2, "severity_text"=>"INFO", "trace_id"=>"\xc4\x13\xd5\xb5\xfe\xa3es%\xfff3 \xc7\xfd\x10", "span_id"=>"we\x1b\xbd\\xe0\xce\x99"}}, {"specversion"=>"1.0", "id"=>"3c344379-2eee-404b-b144-79ffbee05861"}]
```
- S3 file content:
```{"__internal__":{"group_attributes":{"resource":{"attributes":{"service.name":"my.service"}},"scope":{"name":"my.library","version":"1.0.0","attributes":{"my.scope.attribute":"some scope attribute"}}},"log_metadata":{"otlp":{"observed_timestamp":1774878509650000000,"severity_number":2,"severity_text":"INFO","trace_id":"\u0013\u0575es%f3 \u0010","span_id":"we\u001b\\\u0399"}}},"specversion":"1.0","id":"3c344379-2eee-404b-b144-79ffbee05861"}```

In the above trace_id and span_id look like they were saved byte arrays formatted to i.e. UTF-8. When parsed into byte arrays and then into hex strings they present like this:
trace_id: ee838413d5b5ee83beee82a3657325ee83bf663320ee838710
span_id: 77651bee82bd5cee83a0ce99

which is quite different than the input.

**Your Environment**
* Version used: 4.2.2 and 4.2.3 (one from 5.0.0 docker image)
* Configuration:

```yaml
service:
  flush: 1
  grace: 30
  log_level: debug
  hot_reload: on
  http_server: on
  http_port: 2020
  health_check: on

pipeline:
  inputs:
    - name: opentelemetry
      port: 4318
      buffer_max_size: 10MB
      buffer_chunk_size: 512KB

  filters:
    - name: stdout
      match: '*'

  outputs:
     - name: s3
        match: '*'
        retry_limit: 5
        workers: 1
        bucket: "bucket-name"
        region: "s3-region"
        endpoint: "s3.endpoint"
        upload_timeout: 1m
        s3_key_format: /prefix/%Y-%m-%d-%H-%M-%S-$UUID.log
        total_file_size: 1MB
        json_date_key: false
        use_put_object: true
```

**Additional context**
This issue is blocking our ability to filter/group/do anything basically with logs using trace_id and/or span_id. Besides the malformed trace_id sometimes exceeds it's valid size, which results in errors when sending data to OTEL outputs.

Besides that I've noticed that what I see in logs from stdout filter differs between HTTP and GRPC inputs:
- Data sent:
Same log as above but with "traceId": "5B8EFFF798038103D269B633813FC622", "spanId": "EEE19B7EC3C1B122",
- GRPC input: "trace_id"=>"\xe4\x1f\x04\x14Q{\xf7\xcd7\xf3]7\x0fn\xbd\x07\xad\xf7\xf3]\xc5\x0b\xad\x02", "span_id"=>"\x10A5\xf4\x1e\xc4\x0bp\xb5\x07^\xf8"
- HTTPinput: "trace_id"=>"[\x8e\xff\xf7\x98\x03\x81\x03\xd2i\xb63\x81?\xc6\x0c", "span_id"=>"\xee\xe1\x9b~\xc3\xc1\xb1t"
and both logs from GRPC and HTTP have invalid trace_id and span_id.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1e69f3726f9ceddd1beb7c3eb8096a1ca6ce4bc0`.  There
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
{"case_id": "fluent_fluent_bit__11630__1e69f37",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
