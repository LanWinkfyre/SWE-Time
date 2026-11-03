# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[cloudwatch_logs] SIGSEGV when PutLogEvents returns ResourceNotFoundException on an existing stream (plugin crashes instead of recreating/retrying)

Hello,

  The cloudwatch_logs output plugin crashes with SIGSEGV when a PutLogEvents call returns **ResourceNotFoundException ("The specified log stream does not exist")** for a log stream that the plugin had just confirmed as existing (Log Stream ... already exists) milliseconds earlier.

  Instead of recovering from this transient error (recreating the stream and retrying, as retry_limit would suggest), the whole
Fluent Bit process receives a SIGSEGV and dies. Because the FireLens log-router container is essential: false, ECS does not restart it, so the application kept running while all application logs were silently dropped for 8 days before we noticed.

  **Version**
  **- AWS for Fluent Bit Container Image Version: 3.2.5**
  **- Fluent Bit: v4.2.2, commit ddfef360d7**
  **- Built as a custom image on top of the above base.**

  Environment / setup

  - Platform: Amazon ECS with FireLens (FireLens type fluentbit, config-file-value: /extra.conf, enable-ecs-log-metadata: false)
  - Region: eu-west-1
  - Storage: memory (storage_strategy='memory')
  - Log-router container essential: false, memoryReservation: 256
  - The plugin uses dynamic stream creation via log_stream_template: $stream (≈6 distinct streams per service; the affected one,
  uam_rest_hibernate.log, is low-traffic / frequently idle).

  Output configuration (from the application container, awsfirelens log driver)

```
"log-router" = {
          essential          = false
          image              = local.fluentbit_ecr_image_url
          memory_reservation = 256
          cpu                = 128
          restart_policy = {
            enabled              = true
            restartAttemptPeriod = 60
          }
          environment = [
            { name = "DEFAULT_STREAM", value = "uam_rest_out.log" }
          ]
          firelens_configuration = {
            type = "fluentbit"
            options = {
              enable-ecs-log-metadata = "false"
              config-file-type        = "file"
              config-file-value       = "/extra.conf"
            }
          }
        }
```
```
log_configuration = {
            logDriver = "awsfirelens"
            options = {
              Name                = "cloudwatch_logs"
              region              = local.region
              log_group_name      = local.environments[each.key].service.cdw_group
              log_stream_name     = "uam_rest_out.log"
              log_stream_template = "$stream"
              auto_create_group   = "true"
              log_format          = "json"
              retry_limit         = "3"
            }
          }
```

  Logs (exact crash sequence)

```
  [2026/06/10 14:06:30.380] [ info] [output:cloudwatch_logs:cloudwatch_logs.1] Creating log stream uam_rest_hibernate.log in log
  group /aws/logs/<redacted>/uam/rec1
  [2026/06/10 14:06:30.386] [ info] [output:cloudwatch_logs:cloudwatch_logs.1] Log Stream uam_rest_hibernate.log already exists
  [2026/06/10 14:06:30.405] [error] [output:cloudwatch_logs:cloudwatch_logs.1] PutLogEvents API responded with
  error='ResourceNotFoundException', message='The specified log stream does not exist.'
  [2026/06/10 14:06:30]      [engine] caught signal (SIGSEGV)
  [2026/06/10 14:06:30.405] [error] [output:cloudwatch_logs:cloudwatch_logs.1] Failed to send log events
  [2026/06/10 14:06:30.405] [error] [output:cloudwatch_logs:cloudwatch_logs.1] Failed to send log events
```

  Fluent Bit had started cleanly and run for ~30 hours before this crash. No stack trace/backtrace was emitted by the image — happy to re-run with backtrace enabled if you can point me to the flag.

  Additional context (we verified)

  - The stream was not deleted: AWS CloudTrail shows no DeleteLogStream / DeleteLogGroup on this log group around the crash (last manual DeleteLogStream in the account was ~7 weeks earlier on an unrelated group). So ResourceNotFoundException here was a transient/inconsistent response on a stream that existed, not a real deletion.
  - Container exited with exit code 255.

  **Expected behavior**
  When PutLogEvents returns ResourceNotFoundException, the plugin should recreate the missing log stream and retry the batch (within retry_limit), or at worst log the error and continue. It must never SIGSEGV — a single API error response should not crash the whole process and take down log routing for every other stream.

  Impact
  - Total, silent loss of application logs for the affected service until manual restart.
  - Because the log-router is a non-essential sidecar, the crash is invisible without external monitoring.

  **Questions**

  **1. Is this segfault on ResourceNotFoundException in cloudwatch_logs a known issue, and is it fixed in a release newer than AWS for Fluent Bit 3.2.5 / Fluent Bit v4.2.2? If so, which version should we upgrade to?
  2. Any recommended mitigation for transient ResourceNotFoundException with log_stream_template + frequently-idle streams (e.g.,filesystem buffering, config options)?**
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b0fdb50a091b421b44b1d0a75922726c104678d1`.  There
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
{"case_id": "fluent_fluent_bit__11959__b0fdb50",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
