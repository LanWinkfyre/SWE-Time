# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
RFC: Optional server-side context-compression middleware for /v1/chat/completions

### Problem

Long multi-turn conversations regularly exceed a model's context window.
Today LocalAI returns:

```
HTTP 500: request (61234 tokens) exceeds the available context size (32768)
```

The user has to truncate their conversation by hand, losing context.
Client-side workarounds exist (e.g. LibreChat's summarization), but they
duplicate effort across every frontend talking to LocalAI, and they don't
help operator-driven scenarios like the `/v1/mcp/chat/completions` path
or long-lived agent workflows.

### Proposal

Add an **opt-in, per-model middleware** that compresses the head of the
conversation with a fast secondary model when a request approaches
`context_size`. The compressed content is replaced by a single system
message containing the summary. The request is then proxied to the
primary model.

### Config (per model YAML)

```yaml
compression:
  enabled: true
  trigger_at_ratio: 0.75           # compress when request hits 75% of context_size
  keep_tail_tokens: 8000           # never compress the final 8k tokens
  max_summary_tokens: 2048
  compressor_model: "LFM2-24B-A2B-GGUF"    # optional; falls back to primary
  on_post_compression_overflow: "drop_oldest_summary"   # alt: "error"
```

Opt-in, default off. Absent block = no change to existing behavior.

### Flow

1. Middleware reads `config.Compression` after `SetOpenAIRequest`.
2. Counts request tokens via tiktoken-go.
3. Under threshold → pass through.
4. Over → partition into `compress` (head) + `keep` (tail preserving
   `keep_tail_tokens`).
5. Invokes `compressor_model` with a fixed prompt:

   > Summarize the following conversation for an AI agent to continue
   > coherently. Preserve: names, numbers, decisions, URLs, error
   > messages, tool names and their results. Drop: pleasantries,
   > repetition. Max: 500 tokens.

6. Replaces compressed turns with
   `{"role":"system", "content":"[COMPRESSED: <summary>]"}`.
7. If still over context after compression: drops oldest summary and
   retries (configurable). Two consecutive drops → HTTP 413.
8. Proxies transformed request to primary model.
9. Attaches `usage.compression_meta`:

   ```json
   { "original_tokens": 61234, "compressed_tokens": 15120,
     "dropped_turns": 18, "compressor": "LFM2-24B-A2B-GGUF",
     "summary_tokens": 497, "overflow_recoveries": 0 }
   ```

### Prometheus metrics

```
localai_compression_events_total{model, result}     # success | skipped | error
localai_compression_ratio{model}                    # histogram, original/compressed
localai_compression_duration_seconds{model}         # histogram
```

### API compatibility

- Additive only (`compression.*` YAML, `usage.compression_meta` response
  field).
- OpenAI-compat clients ignore unknown `usage.*` keys.
- Applies to both `/v1/chat/completions` and `/v1/mcp/chat/completions`
  (automatic via existing handler delegation in
  `core/http/endpoints/localai/mcp.go:61`).

### Non-goals

- No recursive summarize-summaries (1-pass covers observed needs).
- No persistent compression store (stateless per-request).
- No automatic re-embedding of compressed content.

### Implementation outline

1. Config struct in `core/config/model_config.go:32` (mirrors
   existing `FunctionsConfig`, `ReasoningConfig`, `MCP`).
2. New `pkg/tokens/count.go` wrapping tiktoken-go (already indirect
   in go.mod:413 — promote to direct).
3. Middleware in `core/http/middleware/compression.go` following the
   `trace.go` template, inserted after `SetOpenAIRequest` in the
   `chatMiddleware` chain at `core/http/routes/openai.go:35-51`.
4. Ginkgo tests inline; docs under `docs/content/features/compression.md`.

### Open questions for mudler

1. **Where should `tokens` helper live?** Proposing `pkg/tokens/` —
   reusable by future features. Alternatives: `core/util/tokens/` or
   `internal/tokens/`. Preference?

2. **Prometheus naming** — `localai_compression_*` or `localai_mw_*`
   prefix? Any existing metric-naming convention I should match?

3. **Compressor model resolution** — if `compressor_model` is set but
   not loaded, should middleware (a) skip compression and pass through
   with a warning, (b) try loading via model loader, (c) error? Our
   production default is (a).

4. **SSE streaming requests** — compression operates on the request
   pre-send, so streaming the response is unaffected. Sound?

### Prior art

This design is based on 3+ months of production use at walcz.de (in a
Python proxy called `prompt-optimizer`). The 1021-LOC Python reference
implementation handles token counting, partition logic, multi-message
tool-chain preservation, and overflow recovery. Happy to share for
reference if helpful.

### Next step

If the design lands, I'll submit a PR with:

- `pkg/tokens/count.go` + tests (can merge independently)
- `CompressionConfig` + middleware + metrics + tests
- `docs/content/features/compression.md`

Approx 3-5 days of work.

Assisted-by: Claude:claude-opus-4-7
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4058194b18b0bda486dbcc4aa5b01931a212eecd`.  There
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
{"case_id": "mudler_LocalAI__9534__4058194",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
