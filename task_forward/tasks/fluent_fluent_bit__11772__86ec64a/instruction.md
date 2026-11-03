# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
log_to_metrics: Counter mode stops emitting/stalls after several hours while Histogram continues to work (v4 and 5)

**Description**
Fluent Bit Version: 4.2.3 (Deployed via Docker Swarm)

**Summary:**
There appears to be a bug in the log_to_metrics filter's counter path. After running for several hours (ranging from 1 to 5 hours), the filter in metric_mode counter stops passing data to its internal emitter, effectively "stalling" the metric. Curiously, a second log_to_metrics filter in metric_mode histogram, processing the exact same input records with the same labels, continues to function perfectly without any interruption.

This issue was previously raised in the documentation repository, where it was acknowledged as a likely bug in the plugin's code rather than a configuration error.

Reference to documentation discussion:
https://github.com/fluent/fluent-bit-docs/issues/2551#issuecomment-4363417568

> Quote from Maintainer: "The real problems looks like a bug in the filter's counter path.... so can you raise this on the fluent-bit project please?"

`
### THIS ONE STOPS WORKING (Counter)
    - name: log_to_metrics
      alias: nginx_request_status_code_total
      match: 'nginx.b2b.access'
      tag: metrics.nginx
      emitter_name: em_status_code
      flush_interval_sec: 10
      metric_mode: counter
      metric_name: nginx_request_status_code_total
      label_field:
        - request_method
        - status
        - host
        - endpoint
        - hostname

    #### THIS ONE CONTINUES WORKING (Histogram)
    - name: log_to_metrics
      alias: nginx_http_request_duration_seconds
      match: 'nginx.b2b.access'
      tag: metrics.nginx
      emitter_name: em_request_duration
      flush_interval_sec: 10
      metric_mode: histogram
      metric_name: nginx_http_request_duration_seconds
      value_field: upstream_response_time
      bucket: [0.1, 0.5, 1.0, 5.0, 10.0]
      label_field:
        - request_method
        - status
        - host
        - endpoint
        - hostname
`
Observations & Debug Data
API Metrics Output: Inspecting http://localhost:2020/api/v1/metrics shows that the filter records for the Counter alias continue to increment, but the corresponding input emitter (em_status_code) stops receiving records (records and bytes stay at 0).

Buffer/Memory: Increasing emitter_mem_buf_limit to 128M and setting Retry_Limit for the output had no effect. The emitter stalls even when memory buffers are well within limits.

Cardinality: The number of unique label combinations is low (~20-50), ruling out typical high-cardinality memory exhaustion.

Behavior: 5XX and 4XX status codes (lower frequency) usually disappear first, followed by 200 codes.

Steps to Reproduce
Configure two log_to_metrics filters (Counter and Histogram) on a high-traffic stream (~4k rec/s).

Monitor output via Prometheus/VictoriaMetrics.

Observe that after 1-5 hours, the counter metrics disappear or flatten to zero, while histograms remain active.

Expected Behavior
Both counter and histogram modes should reliably emit data as long as the filter receives records.

Actual Behavior
The counter mode internal state/emitter stalls, while the histogram mode remains fully functional on the same data stream.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `86ec64a170bfa4984c963a8e76ffc0453be1caf2`.  There
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
{"case_id": "fluent_fluent_bit__11772__86ec64a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
