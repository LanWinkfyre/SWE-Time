# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: OpenTelemetry trace export for agent runs (agentic-first observability)

## Problem

Waza emits internal session events but doesn't expose them in any industry-standard shape. Authors and platform teams who already run an OTel-compatible backend (Aspire, Jaeger, Tempo, Application Insights, Honeycomb, Datadog) can't drop waza into their existing observability pipeline.

Result: a debugging session means staring at `results.json` and transcripts instead of using familiar trace UIs.

## Proposal

Add an opt-in OpenTelemetry exporter for agent runs:

- `waza run --otel-exporter <otlp|stdout|file>` plus `--otel-endpoint`, `--otel-headers`.
- Emit spans following the [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/): `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.tool.name`, etc.
- Span hierarchy: `eval` → `task` → `turn` → `tool_call` / `model_call`.
- Default-off; default redaction policy strips prompt/tool-arg/output content unless `--otel-include-payloads` is set.
- Best-effort trace ID propagation: preserve trace IDs *if* the engine surfaces them; do not require Copilot SDK changes.

## Why this matters for agentic-first

Agentic runs are graph-shaped (turns × tools × sub-agents). Flat logs hide the structure. OTel traces are how the rest of the industry navigates this shape, and exporting them means waza fits into the observability stack teams already pay for.

## Acceptance criteria

- [ ] OTel exporter integrated; off by default.
- [ ] Spans conform to `gen_ai.*` semantic conventions; schema-test verifies attribute names without requiring a live backend.
- [ ] Default redaction strips prompt/tool-arg/output content; opt-in flag to include them.
- [ ] Works with at least OTLP/HTTP and stdout exporters.
- [ ] No new required dependency for users who don't enable it.
- [ ] Docs in `site/` with an example wiring to a local collector.
- [ ] Tests assert span shape and redaction behavior.

## Non-goals (filed separately)

- Live SSE streaming — see #178.
- Replay/snapshot artifacts — see #367 (complementary, not blocking).
- Dashboard rendering of OTel traces — handled by external backends.

## Related

- Engine event abstraction: #10
- SSE live events: #178
- Snapshot/replay: #367
- Roadmap: #66
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5af9038ba478c9bca700a4f71a847db85a85a7b9`.  There
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
{"case_id": "microsoft_waza__362__5af9038",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
