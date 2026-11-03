# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
RFC: Optional per-model PII replacement middleware (regex-based, bijective)

### Problem

Operators who route LocalAI traffic to a model whose backend sits outside
their trust boundary (a remote hosted endpoint, a partner's service, a
sidecar that logs) have no server-side mechanism to scrub and restore
PII inside LocalAI's request/response path. Today they rewrite it
outside LocalAI or simply don't route sensitive content at all.

### Proposal

Add an **opt-in, per-model middleware** that performs bijective token
substitution:

- Scans outgoing request messages for **regex-detectable** PII
- Replaces matches with deterministic tokens
  (`Peter Müller` → `PERSON_001`)
- Forwards the transformed request to the model
- Reverses substitutions in the response (stream + non-stream) before
  the client sees it

**Framing**: this is PII replacement, not a compliance tool. Operators
remain responsible for legal/retention/audit concerns. No claims about
GDPR/HIPAA are made or implied by this feature.

### Config (per-model YAML)

```yaml
pseudonymization:
  enabled: true
  detectors: []                    # default empty; operator lists explicitly
  strategy: deterministic          # same input → same token within request
  reverse_in_response: true
```

Detector names available in Phase 1:
- `regex_email`
- `regex_phone_de`
- `regex_phone_intl`
- `regex_hrb` (German Handelsregister)
- `regex_iban`

**Scope**: middleware activates only when `enabled: true` on that model.
No global trigger. No "outgoing request" heuristic. Operator picks models
explicitly (e.g. only `claude-opus-4-7.yaml`, not others).

### Flow

**Request side (after `SetOpenAIRequest`):**
1. Run enabled detectors in declared order.
2. Build bijective in-memory map (scope: one request).
3. Replace in message content.
4. Attach map to Echo context (`defer`-released).
5. Forward to model.

**Response side (Echo response-writer wrapper):**
1. Read map from Echo context.
2. Wrap response writer; intercept SSE chunks + final body.
3. Reverse token substitutions with sliding-window buffering for
   multi-chunk tokens (e.g. `PERSON_001` split across SSE frames).
4. On client-disconnect, `defer` releases map — no leak.

### Architecture — why response-writer wrapper, not inline edit

An earlier draft considered modifying `core/http/endpoints/openai/chat.go`
inside the streaming loop where `ev.Choices[0].Delta.Content` is set
(around L682-689). We rejected that: it couples this feature to that
specific streaming implementation, and any upstream change there
would force a merge-conflict on our middleware.

An Echo response-writer wrapper (same pattern Echo's `BodyDump` uses,
but with a transformer instead of a sink) keeps the seam at the
middleware layer. Willing to go the other direction if maintainers
prefer — this is worth discussing early, hence the RFC.

### Metadata

Response adds:

```json
{
  "usage": {
    "pseudonymization_meta": {
      "detectors_fired": ["regex_email", "regex_phone_de"],
      "tokens_replaced": 7,
      "request_round_trip": true
    }
  }
}
```

No salt, no map, no user-content hash leaves the server.

### Non-goals (Phase 1)

- **No NER.** spaCy / LLM-as-NER path is a Phase 2 PR. Keeps this one
  small and review-focused on the regex + middleware seam.
- No UI management (YAML only).
- No cross-request mapping persistence (Redis/TTL is a Phase 2 feature).
- Not a DLP tool. Not an anonymization tool (round-trip is bijective
  by design).

### Prometheus metrics (proposal)

```
localai_pii_detections_total{model, detector}
localai_pii_replacements_total{model}
localai_pii_stream_buffer_overflow_total{model}   # diagnostic for tuning
```

### Implementation outline

1. `PseudonymizationConfig` in `core/config/model_config.go:32` (mirrors
   `FunctionsConfig`, `ReasoningConfig`, `MCP` at L61-92).
2. New `pkg/pii/` package:
   - `detector.go` interface + registry
   - `regex.go` detector implementations
   - `engine.go` bijective map + apply/reverse
3. Request middleware at `core/http/middleware/pseudonymization_request.go`.
4. Response middleware at `core/http/middleware/pseudonymization_response.go`
   (Echo writer-wrapper with sliding buffer).
5. Both appended to `chatMiddleware` at
   `core/http/routes/openai.go:35-51`. MCP endpoint picks them up via
   existing `core/http/endpoints/localai/mcp.go:61` delegation.
6. Ginkgo tests inline. Docs `docs/content/features/pseudonymization.md`
   with a security-caveat banner at the top.

### Open questions for mudler

1. **Response-writer wrapper vs. inline edit** — preference? We lean
   wrapper for maintenance durability; willing to go inline if you
   see a cleaner path.

2. **`pkg/pii/` placement** — new top-level package, or `internal/pii/`?
   Regex detectors are narrow enough that reuse across LocalAI is
   unlikely, but we'd like to keep it swappable.

3. **Detector naming convention** — `regex_email` vs `email_regex` vs
   `pii.email.regex`? Whatever matches your house style for future
   detector adds.

4. **Metric naming prefix** — `localai_pii_*` or share a prefix with
   compression PR's `localai_compression_*`? Should all middleware
   metrics live under `localai_middleware_*`?

5. **Default behavior of unknown detector names in YAML** — error
   startup, warn-and-skip, or accept (future detector names)? We lean
   error-at-startup so operator typos are caught early.

### Prior art

walcz.de production runs this pattern in Python (`prompt-optimizer`)
for 4 months across 17 agents. The 195-LOC `pseudonymizer.py` and
regex portions of `pii_detector.py` (349 LOC total, regex ≈150 LOC)
are the basis. German business correspondence (Müller, HRB, IBAN DE89)
stress-tested. Happy to share code for reference.

### Next step

If this design lands, PR submission plan:

- Commit 1: `pkg/pii/` regex detector + bijective engine + tests
  (can merge as a utility library, independent of middleware)
- Commit 2: Request + response middleware + config + tests + docs

Approx 4-6 days total.

Assisted-by: Claude:claude-opus-4-7
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `359bd4850d90af9165cade9cf72df85017872975`.  There
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
{"case_id": "mudler_LocalAI__9535__359bd48",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
