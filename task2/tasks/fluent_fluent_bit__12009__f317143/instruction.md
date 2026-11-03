# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_tail: SIGSEGV in flb_lib_worker (flb_lib.c:909) persists on 5.0.8 under HTTP/OSIS 408 + circuit-breaker backpressure (follow-up to #11954)

## Summary

Follow-up to #11954 (filing as a separate issue with our configuration, as requested by @cosmo0920).

We still hit the `flb_lib_worker` SIGSEGV on **5.0.8** — the release that contains the #11956 timer-lifecycle fix. Same stack trace as #11954. It reproduces on a Kubernetes DaemonSet under sustained HTTP-output backpressure (AWS OpenSearch Ingestion / OSIS returning `408` → circuit breaker opens), with `tail` inputs using `threaded on` + filesystem storage. (#11954 attributes the crash to the tail input; our stack trace is identical — though we have not ourselves tested with the tail input removed.)

## Version / environment

- Fluent Bit **5.0.8**, official image `fluent/fluent-bit:5.0.8`
- Kubernetes DaemonSet, ~100+ Linux nodes (amd64 + arm64)
- **Our deployment history:** we ran **5.0.3** in production for a long time with no such crashes, then upgraded **directly to 5.0.8** and began hitting this SIGSEGV. We did **not** run any intermediate release (5.0.4–5.0.7) ourselves.
- **Regression window (from #11954 + a source-tree bisect, not our own testing):** the original report pins it between **5.0.5 (stable)** and **5.0.6 (crashes)**. We corroborated this against the source: the `reconcile_file_state` / progress-check timer code added by #11750 is absent in `v5.0.5` and present from `v5.0.6` onward. #11956 (in 5.0.8) was the fix attempt but does not resolve it for our path.

## Sequence observed

1. The `http` output (OSIS) begins returning `408` and the circuit breaker opens:
   ```
   [error] [output:http:http.1] <pipeline>.us-west-2.osis.amazonaws.com:443, HTTP status=408
   Circuit breaker is open. Unable to write to buffer.
   [error] [output:http:http.1] <pipeline>.us-west-2.osis.amazonaws.com:443, HTTP status=408
   Circuit breaker is open. Unable to write to buffer.
   ```
2. ~1 minute later, SIGSEGV (same frame as #11954; stripped binary so only `flb_lib_worker` symbolized):
   ```
   [engine] caught signal (SIGSEGV)
   #0  0x...  in  flb_lib_worker() at src/flb_lib.c:909
   #1  0x...  in  ???() at ???:0
   #2  0x...  in  ???() at ???:0
   ```
3. After the automatic restart, the `s3` filesystem buffer size counter underflows:
   ```
   [error] [output:s3:s3.2] Buffer is full: current_buffer_size=18446744073549369344, store_dir_limit_size=10000000000 bytes
   ```
   `18446744073549369344` ≈ `2^64 − ~160 MB` — an unsigned underflow. The S3 output then refuses all buffering (`Could not buffer chunk`), chunks back up, and the pod goes NotReady (health check returns 500). This secondary state clears on a manual pod delete (store_dir is re-scanned on startup). It appears to be a downstream consequence of the unclean shutdown from the crash, rather than an independent issue.

## Configuration (sanitized)

Minimal subset exercising the crash path (filesystem storage + a `threaded` tail input + a backpressuring HTTP output):

```ini
[SERVICE]
    Flush 1
    storage.path /var/log/fluent-bit/
    storage.max_chunks_up 128
    storage.backlog.mem_limit 100M

# tail input — threaded + filesystem-backed (the crash is in this path; Inotify_Watcher at default On)
[INPUT]
    Name tail
    Path /var/log/containers/*.log
    multiline.parser cri
    Read_From_Head True
    DB /var/log/fluent-bit/tail-containers.db
    storage.type filesystem
    threaded on

# HTTP output to AWS OSIS — backs up (408 -> circuit breaker), creating the backpressure that precedes the crash
[OUTPUT]
    Name http
    Match *
    Host <pipeline>.us-west-2.osis.amazonaws.com
    Port 443
    URI /log/ingest
    Format json
    aws_auth true
    aws_region us-west-2
    aws_service osis
    tls On
    storage.total_limit_size 5G

# S3 output — filesystem-buffered; its size counter underflows after the crash restart
[OUTPUT]
    Name s3
    Match *
    bucket <s3-logs-bucket>
    region us-west-2
    use_put_object on
    store_dir /var/log/fluent-bit/s3
    store_dir_limit_size 10G
```

Our full production config additionally has `tail` (kube-audit) and `systemd` inputs, `kubernetes`/`lua`/`modify`/`rewrite_tag` filters, and a second `s3` output — all available on request.

## Questions for maintainers

1. #11956 (in 5.0.8) was meant to fix the `in_tail` progress-check timer lifecycle, but the SIGSEGV still occurs for us on 5.0.8. Is there a remaining path (e.g. under `threaded on` + filesystem storage + heavy HTTP-output backpressure) not covered by that fix?
2. Does `Inotify_Watcher Off` **fully** avoid the crashing code path on 5.0.8, or only reduce frequency? We can apply it as a workaround but want to confirm it's a complete mitigation rather than pinning to an older release (we've rolled back to 5.0.3 for now).

Happy to provide full `debug`-level logs or a core dump if that helps.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f31714397e1797208d64e9aacfd43ee00cd8505c`.  There
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
{"case_id": "fluent_fluent_bit__12009__f317143",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
