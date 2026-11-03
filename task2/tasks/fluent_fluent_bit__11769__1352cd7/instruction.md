# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
http_server: built-in HTTP server deadlocks when exec input curls Fluent Bit internal endpoints

## Bug Report

**Describe the bug**
In Fluent Bit v5.0.x, the built-in HTTP server (port 2020) deadlocks when any pipeline component makes an HTTP request to it from within the main event loop.

**To Reproduce**
Minimal config:

```ini
[SERVICE]
    HTTP_Server  On
    HTTP_Listen  0.0.0.0
    HTTP_Port    2020
    Flush        1

[INPUT]
    Name         exec
    Tag          test
    Command      curl -s http://127.0.0.1:2020/api/v1/metrics/prometheus
    Interval_Sec 30

[OUTPUT]
    Name  null
    Match *
```

1. Start Fluent Bit, confirm the health check works:

```sh
curl http://127.0.0.1:2020/api/v1/uptime   # works fine
```

2. Wait 30s for exec to fire, then try again:

```sh
curl http://127.0.0.1:2020/api/v1/uptime   # hangs forever
```

This works fine on v1.9.x and v4.2.x, but breaks on every v5.0.x release I've tested (v5.0.0 through v5.0.4).

**Expected behavior**
The built-in HTTP server should remain responsive while the `in_exec` plugin is running, as it did in v1.9.x and v4.2.x.

**Screenshots**
N/A

**Your Environment**
* Version used: broken in v5.0.0 through v5.0.4, works in v1.9.10 and v4.2.2
* Configuration: see minimal config above
* Environment name and version: ECS Fargate (ARM64), also reproduced locally on macOS
* Server type and version: N/A
* Operating System and version: Amazon Linux 2023 (Fargate), macOS 15 (local)
* Filters and plugins: `in_exec`, `out_null` (minimal repro)

**Additional context**
My use case is emitting Fluent Bit internal metrics out as CloudWatch metrics. The flow is (1) scrape Fluent Bit metrics endpoint with `in_exec`, (2) transform metrics into CloudWatch embedded metric format via `filter_lua`, and then (3) emit to CloudWatch as logs via `out_cloudwatch_logs`, which CloudWatch automatically converts to metrics.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1352cd7378ab2e44f5311fc213c11216789134d5`.  There
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
{"case_id": "fluent_fluent_bit__11769__1352cd7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
