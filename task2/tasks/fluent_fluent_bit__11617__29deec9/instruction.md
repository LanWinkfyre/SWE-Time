# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
retain_metadata_in_forward_mode is not working in upstream configuration

# Bug Report: `retain_metadata_in_forward_mode` in upstream config

## Describe the bug

Setting `retain_metadata_in_forward_mode true` on a **forward output upstream** `[NODE]` does not preserve record metadata when data is sent from one Fluent Bit instance to another over the forward protocol. Nested structures such as `__internal__` (including OTLP-derived `log_metadata`, trace/span IDs, attributes, etc.) are dropped on the receiving Fluent Bit, even though the option is intended to retain forward-mode metadata across hops.

Observed when using the HA upstream file mounted at `/fluent-bit/etc/forward/satellite-forward-lb` for forward outputs that reference `upstream: /fluent-bit/etc/forward/satellite-forward-lb`.

## To Reproduce

- **Rubular link:** N/A

- **Example log message (sender FB1 — `fluentbit-1`):**

```json
{"date":1774341343.539138,"__internal__":{"group_attributes":{"resource":{"attributes":{"telemetry.sdk.language":"python","telemetry.sdk.name":"opentelemetry","telemetry.sdk.version":"1.40.0","service.name":"fb-poc-app","service.version":"1.0.0","deployment.environment":"development"},"schema_url":""},"scope":{"name":"root"}},"log_metadata":{"otlp":{"observed_timestamp":1774341342223670467,"timestamp":1774341342223117568,"severity_number":9,"severity_text":"INFO","attributes":{"code.file.path":"/app/app.py","code.function.name":"home","code.line.number":128},"trace_id":"\u001f\u0019\u0006\u0005\u0017b72\u0014\u001a","span_id":"L\b/7","trace_flags":1}}},"log":"Home endpoint accessed"}
```

- **Same record on receiver FB2 — `fluentbit-2-1` / `fluentbit-2-2` (stdout debug):**

```json
{"date":1774341343.539138,"log":"Home endpoint accessed"}
```

- **Upstream file** (`configs/fluent-bit-1/forward/satellite-forward-lb`):

```ini
# HA upstream file loaded by forward output when upstream: /fluent-bit/etc/forward/satellite-forward-lb
[UPSTREAM]
    name       satellite-forward-lb

[NODE]
    name                            node-1
    host                            fluentbit-2-1
    port                            24228
    require_ack_response            false
    compress                        gzip
    retain_metadata_in_forward_mode true
    send_options                    true

[NODE]
    name                            node-2
    host                            fluentbit-2-2
    port                            24229
    require_ack_response            false
    compress                        gzip
    retain_metadata_in_forward_mode true
    send_options                    true
```

- **Steps to reproduce:**

  1. Run the Docker Compose stack in this repo (`docker compose up`) so `fb-poc-app` sends OTLP logs to `fluentbit-1` and forward traffic reaches `fluentbit-2-*`.
  2. Configure a forward output on the sender to use the upstream file above (or an equivalent minimal repro with two FB instances and `retain_metadata_in_forward_mode true` on an upstream node).
  3. Ensure `send_options: true` on the forward output (required for the options/metadata path).
  4. Compare records on the sender vs. receiver (e.g. `stdout` with `format: json_lines` on FB2).
  5. Observe that `__internal__` and nested OTLP metadata are missing on the receiver despite `retain_metadata_in_forward_mode true` on the upstream node.

## Expected behavior

When `retain_metadata_in_forward_mode` is set to `true` on the forward output’s upstream node, the full record shape—including forward-mode metadata such as `__internal__` and nested OTLP/log metadata—should be preserved across the forward hop so the receiver sees the same fields as the sender (within documented limitations), not only top-level keys like `date` and `log`.

## Screenshots

N/A — JSON examples above show before/after.

## Your Environment

| Item | Details |
|------|---------|
| **Fluent Bit version** | Image: `fluent/fluent-bit:4.2.3.1` (tag not pinned to a digest in `docker-compose.yml`). **To capture exact build for the issue:** `docker compose exec fluentbit-1 /fluent-bit/bin/fluent-bit --version` |
| **Configuration** | YAML: `configs/fluent-bit-1/fluent-bit.yaml`, `configs/fluent-bit-2/fluent-bit.yaml`; upstream: `configs/fluent-bit-1/forward/satellite-forward-lb` |
| **Environment** | Docker Compose; services: `fluentbit-1`, `fluentbit-2-1`, `fluentbit-2-2`, `otel-collector`, `prometheus`, `vector`, `app` |
| **Host OS (dev)** | macOS (Darwin 24.x) — containers run Linux |
| **Filters and plugins** | **FB1 inputs:** `opentelemetry` (logs :4417, traces :4418 with tail sampling), `prometheus_remote_write` (:9882). **FB1 outputs:** `forward` (with `send_options`, `retain_metadata_in_forward_mode`, `compress: gzip` where configured), `stdout` (debug). **FB2 inputs:** `forward` (:24228, :24229). **FB2 outputs:** `opentelemetry` to collector, `prometheus_remote_write`, `stdout` (debug). |

### Additional configuration notes (this repo)

- Forward outputs that use `upstream: /fluent-bit/etc/forward/satellite-forward-lb` include `v1_traces` and `prometheus_rw` in `configs/fluent-bit-1/fluent-bit.yaml`. The `v1_logs` match currently uses explicit `host`/`port` to `fluentbit-2-1`; if reproducing strictly via upstream for logs, point the logs forward output at the same upstream file and compare behavior.
- App sends OTLP logs to `http://fluentbit-1:4417/v1/logs` (`fb-poc-app` env in `docker-compose.yml`).

## Additional context

This blocks preserving trace context, severity, attributes, and OTLP-derived fields across a multi-hop Fluent Bit topology (FB1 → FB2). Downstream components (e.g. OpenTelemetry output on FB2 with `logs_trace_id_metadata_key` / `logs_span_id_metadata_key`) depend on metadata surviving the forward hop.

Please clarify whether `retain_metadata_in_forward_mode` on an **upstream** `[NODE]` is fully supported (vs. only on inline forward outputs), and whether `__internal__` is in scope for retention—or document limitations and fix if this is unintended.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `29deec9e72a5e1ccc9996a58481bc7ba4d60353d`.  There
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
{"case_id": "fluent_fluent_bit__11617__29deec9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
