# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out_azure_logs_ingestion: oauth2 token retrieval fails on v5.0.0, works on v4.2.3

## Bug Report

**Describe the bug**

The `azure_logs_ingestion` output plugin fails to retrieve oauth2 access tokens on Fluent Bit v5.0.0. Debug logs show `token expired. getting new token` followed immediately by `error retrieving oauth2 access token`, but no `[oauth2] HTTP Status=...` lines appear — the oauth2 HTTP request to `login.microsoftonline.com` is never initiated. The failure is internal to the oauth2 client.

Downgrading to v4.2.3 with the identical configuration and credentials resolves the issue — tokens are retrieved and logs are ingested successfully (HTTP 204).

Credentials are confirmed valid via direct curl from the same device:

```bash
curl -s -X POST 'https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token' \
  -d 'grant_type=client_credentials&client_id=<id>&client_secret=<secret>&scope=https://monitor.azure.com/.default'
# Returns valid Bearer token
```

**To Reproduce**

Steps to reproduce the problem:

1. Configure `azure_logs_ingestion` output with valid `tenant_id`, `client_id`, `client_secret` (plaintext in YAML, not env vars)
2. Install Fluent Bit v5.0.0
3. Start the service with `log_level: debug`
4. Observe repeated token failure with no oauth2 HTTP activity:

```
[debug] [output:azure_logs_ingestion:azure_logs_ingestion.0] token expired. getting new token
[error] [output:azure_logs_ingestion:azure_logs_ingestion.0] error retrieving oauth2 access token
```

5. Downgrade to v4.2.3: `apt-get install fluent-bit=4.2.3 --allow-downgrades`
6. Restart with the same config — tokens are retrieved, logs ingested:

```
[debug] [output:azure_logs_ingestion:azure_logs_ingestion.0] create token header string
[debug] [output:azure_logs_ingestion:azure_logs_ingestion.0] enabled payload gzip compression
[info] [output:azure_logs_ingestion:azure_logs_ingestion.0] http_status=204, dcr_id=dcr-..., table=IoTLogs_CL
```

**Expected behavior**

The oauth2 token should be retrieved successfully from `login.microsoftonline.com`, as it is on v4.2.3 with the same configuration and credentials.

**Screenshots**

N/A — debug log output included above.

**Your Environment**

* Version used: v5.0.0 (broken), v4.2.3 (works)
* Configuration (simplified):
```yaml
service:
  flush: 1
  daemon: off
  log_level: debug
  scheduler.cap: 60
  scheduler.base: 3

pipeline:
  inputs:
    - name: dummy
      tag: test
      dummy: '{"message": "hello"}'

  outputs:
    - name: azure_logs_ingestion
      match: "*"
      dce_url: https://<dce>.germanywestcentral-1.ingest.monitor.azure.com
      dcr_id: dcr-<id>
      table_name: IoTLogs_CL
      tenant_id: <tenant>
      client_id: <client>
      client_secret: <secret>
      compress: true
      retry_limit: 100
```
* Environment name and version: Bare-metal embedded Linux (not Kubernetes)
* Server type and version: ARM64 embedded computer (aarch64)
* Operating System and version: Ubuntu 22.04
* Filters and plugins: `azure_logs_ingestion` output, `tail` / `systemd` / `docker_events` inputs, various `modify` / `nest` / `lua` / `rewrite_tag` / `grep` / `parser` filters

**Additional context**

Under sustained retry load on v5.0.0 (when many chunks are queued and the oauth2 failure prevents any from flushing), the process eventually segfaulted inside the plugin's format function:

```
#0  msgpack_unpack_next()        at lib/msgpack-c/src/...
#1  flb_log_event_decoder_next() at src/flb_log...
#2  flb_mp_count_log_records()   at src/flb_mp.c:...
#3  az_li_format()               at plugins/out_azure_logs_in...
#4  cb_azure_logs_ingestion_flush()
#5  co_switch()                  at lib/monkey/deps/flb_libco/aa...
```

This may be a separate issue (possibly a corrupted chunk from the FD exhaustion that preceded it), but is noted for completeness.

The `out_stackdriver: clean up oauth2 cache lifecycle` fix in the v4.2.3 release notes suggests related oauth2 lifecycle work has been done recently — the v5.0 branch may be missing this or have a different regression in the same area.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a42e322cfeca73cc7dfd2719e30c21d5de2c42c4`.  There
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
{"case_id": "fluent_fluent_bit__11649__a42e322",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
