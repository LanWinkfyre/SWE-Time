# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Add missing opentelemetry-exporter-otlp-proto-grpc dependency

## Bug

The `opentelemetry-instrument` wrapper defaults to gRPC for trace/metrics export (`otlp_proto_grpc`), but only `opentelemetry-exporter-otlp-proto-http` is listed as a dependency. This causes auto-instrumentation to fail at startup:

```
RuntimeError: Requested component 'otlp_proto_grpc' not found in entry point 'opentelemetry_traces_exporter'
```

Traces are silently lost and the server falls back to running without instrumentation.

## Fix

Add `opentelemetry-exporter-otlp-proto-grpc>=1.30.0` to `pyproject.toml` dependencies alongside the existing HTTP exporter.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1206e31e399b658b0b033981538850c60ae5874c`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "ogx_ai_ogx__6030__1206e31",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
