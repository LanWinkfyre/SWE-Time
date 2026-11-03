# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Realtime: text-only request via beta field `modalities` is silently ignored; defaults to audio/TTS

## Summary

LocalAI’s OpenAI-compatible Realtime WebSocket (`/v1/realtime`) **silently ignores text-only modality requests** when the client uses the widely circulated **beta** field name `modalities` (instead of GA `output_modalities`). The server then **defaults to audio**, runs TTS, and emits large `response.output_audio.*` frames even though the client asked for text only.

When the client sends the **GA** field `output_modalities: ["text"]`, LocalAI correctly skips TTS and emits `response.output_text.*` only.

This is an interoperability footgun: many clients (OpenAI beta examples, third-party SDKs, and custom WS clients) still send `session.modalities` / `response.modalities`. LocalAI drops the unknown JSON key with no error, so clients believe they configured text-only while the pipeline still synthesizes audio (~100KB+ base64 per short reply).

## Environment

- Endpoint: LocalAI Realtime WS `wss://<host>/v1/realtime?model=realtime`
- Model id: `realtime` (pipeline: LLM + TTS + transcription backends)
- Protocol header: `OpenAI-Beta: realtime=v1`
- Reproduced against current LocalAI `master` source layout (files cited below)

## Expected (OpenAI Realtime text-only)

Per LocalAI’s own type comments and OpenAI GA docs:

- `output_modalities: ["text"]` → **no audio / no TTS**
- Client receives `response.output_text.delta` / `response.output_text.done`
- Does **not** receive `response.output_audio.delta`

LocalAI documents this intent here:

```go
// core/http/endpoints/openai/types/types.go
// The set of modalities the model can respond with. It defaults to ["audio"],
// indicating that the model will respond with audio plus a transcript.
// ["text"] can be used to make the model respond with text only.
OutputModalities []Modality `json:"output_modalities,omitempty"`
```

```go
// core/http/endpoints/openai/realtime.go
// OutputModalities mirrors the OpenAI Realtime spec field of the same
// name. Empty means "use the spec default" (audio). ["text"] suppresses
// TTS so the client receives only response.output_text.* events.
```

## Actual

### A) Client sends beta field `modalities: ["text"]` (common)

**Client → server**

```json
{"type":"session.update","session":{"modalities":["text"],"instructions":"Reply with exactly: TEXT_ONLY_OK"}}
{"type":"conversation.item.create","item":{"type":"message","role":"user","content":[{"type":"input_text","text":"Say TEXT_ONLY_OK"}]}}
{"type":"response.create","response":{"modalities":["text"]}}
```

**Server `session.updated`** (note: no `output_modalities` applied; only instructions changed):

```json
{
  "id": "sess_…",
  "object": "realtime.session",
  "audio": {
    "input": {
      "turn_detection": {"type":"server_vad","create_response":true,…},
      "transcription": {"model":"lfm2.5-audio-1.5b-realtime"}
    },
    "output": {}
  },
  "instructions": "Reply with exactly: TEXT_ONLY_OK",
  "model": "realtime",
  "type": "realtime"
}
```

**Server response events (audio path):**

```
conversation.item.added
response.created
response.output_item.added          // content type: output_audio + transcript
response.content_part.added
response.output_audio_transcript.delta   // "TEXT_ONLY_OK"
response.output_audio_transcript.done
response.output_audio.delta              // ~100KB base64 PCM
response.output_audio.done
response.content_part.done
response.output_item.done
response.done
```

- `HAS_OUTPUT_AUDIO_DELTA = true`
- `HAS_OUTPUT_TEXT_DELTA = false`

### B) Client sends GA field `output_modalities: ["text"]` (works)

**Client → server**

```json
{"type":"session.update","session":{"output_modalities":["text"],"instructions":"Reply with exactly: TEXT_ONLY_OK"}}
{"type":"response.create","response":{"output_modalities":["text"]}}
```

**Server `session.updated`:**

```
output_modalities = ["text"]
```

**Server response events (text-only path):**

```
response.output_text.delta
response.output_text.done
… (no response.output_audio.*)
```

- `HAS_OUTPUT_AUDIO_DELTA = false`
- `HAS_OUTPUT_TEXT_DELTA = true`

So LocalAI **does** implement text-only correctly — but only when the GA field name is used. The beta field name is silently ignored.

## Root cause in LocalAI source

### 1. Schema only binds GA name `output_modalities`

```go
// core/http/endpoints/openai/types/types.go (RealtimeSession / ResponseCreateParams)
OutputModalities []Modality `json:"output_modalities,omitempty"`
```

There is **no** `json:"modalities"` field on session/response params. Standard `encoding/json` therefore **drops** `"modalities":["text"]` without error.

### 2. Empty modalities default to audio

```go
// core/http/endpoints/openai/realtime.go
func resolveOutputModalities(session, response []types.Modality) []types.Modality {
	if len(response) > 0 {
		return response
	}
	if len(session) > 0 {
		return session
	}
	return []types.Modality{types.ModalityAudio} // default when both empty
}
```

### 3. session.update only copies OutputModalities when non-empty

```go
// core/http/endpoints/openai/realtime.go (~1235)
if len(rt.OutputModalities) > 0 {
	session.OutputModalities = rt.OutputModalities
}
```

Because `rt.OutputModalities` never got the beta field, this is a no-op.

### 4. Response path branches on audio and always TTS when defaulted

```go
// core/http/endpoints/openai/realtime.go (~2418-2496)
modalities := resolveOutputModalities(session.OutputModalities, respMods)
if modalitiesContainAudio(modalities) {
	// emit response.output_audio_transcript.*
	// emitSpeech → response.output_audio.delta (TTS)
} else {
	// Text-only: response.output_text.delta / .done only
}
```

With the silent drop of `modalities`, `modalitiesContainAudio` is true via the default, so TTS always runs.

## Why this is a bug (not just “client wrong”)

1. **Silent failure**: wrong field is discarded with no `error` event and no indication in `session.updated` that a modality request was rejected/ignored.
2. **Interop**: OpenAI Realtime beta and a large amount of community sample code use `modalities`. Clients cannot discover the rename without reading LocalAI’s Go types.
3. **Cost / correctness**: text-only chat clients unexpectedly receive ~100KB+ audio frames per turn, which also breaks WS clients that use fixed ~64KB receive buffers (incomplete JSON mid-frame).
4. LocalAI already has the correct text-only branch — the bug is **field acceptance / defaults / observability**, not missing TTS suppression.

OpenAI’s current Python types use GA `output_modalities` as well (`openai.types.realtime.realtime_session_create_request_param.output_modalities`), so LocalAI’s primary field name is correct — but **accepting the legacy alias (or rejecting it loudly)** is still needed for Realtime beta compatibility.

## Suggested fix

1. **Accept legacy alias** on `session.update` and `response.create`:
   - If `modalities` is present and `output_modalities` is empty, treat `modalities` as `output_modalities`.
   - Prefer explicit `output_modalities` when both are present.
2. Optionally add a one-time `warning` / debug log:  
   `ignored unknown session field "modalities"; use "output_modalities"`.
3. Always echo effective `output_modalities` in `session.created` / `session.updated` (even when defaulting to `["audio"]`) so clients can verify what the server resolved.
4. Docs (`docs/content/features/openai-realtime.md`): document text-only setup with `output_modalities: ["text"]` and note beta `modalities` is not bound unless aliased.
5. Regression test in `tests/e2e/realtime_ws_test.go`:
   - `session.update` + `response.create` with **only** `modalities: ["text"]` → no `response.output_audio.delta`, has `response.output_text.delta` (if alias implemented) **or** clear error (if reject-unknown chosen).
   - Control: `output_modalities: ["text"]` → text-only (already intended behavior).

## Minimal reproduction (Python)

```python
import asyncio, json, ssl, websockets

URL = "wss://HOST/v1/realtime?model=realtime"
HEADERS = {"Authorization": "Bearer KEY", "OpenAI-Beta": "realtime=v1"}

async def trial(session_body, response_body):
    sslctx = ssl.create_default_context()
    async with websockets.connect(URL, additional_headers=HEADERS, ssl=sslctx, max_size=16*1024*1024) as ws:
        await ws.send(json.dumps({"type": "session.update", "session": session_body}))
        # drain session.created / session.updated …
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {"type":"message","role":"user",
                     "content":[{"type":"input_text","text":"Say TEXT_ONLY_OK"}]},
        }))
        await ws.send(json.dumps({"type": "response.create", "response": response_body}))
        # observe event types until response.done

asyncio.run(trial(
    {"modalities": ["text"], "instructions": "Reply with exactly: TEXT_ONLY_OK"},
    {"modalities": ["text"]},
))
# → response.output_audio.delta present

asyncio.run(trial(
    {"output_modalities": ["text"], "instructions": "Reply with exactly: TEXT_ONLY_OK"},
    {"output_modalities": ["text"]},
))
# → response.output_text.delta only
```

## Related code pointers

| Area | File | Notes |
|------|------|--------|
| Field schema | `core/http/endpoints/openai/types/types.go` | `OutputModalities` → `json:"output_modalities"` only |
| Default | `core/http/endpoints/openai/realtime.go` `resolveOutputModalities` | empty → `["audio"]` |
| session.update apply | `core/http/endpoints/openai/realtime.go` ~1235 | only copies `OutputModalities` |
| TTS vs text branch | `core/http/endpoints/openai/realtime.go` ~2422–2496 | audio → TTS; else `output_text.*` |
| session.updated echo | `Session.ToServer()` ~207 | emits `OutputModalities` when set |

## Impact

Any Realtime client that sends OpenAI **beta** `modalities: ["text"]` for hub/text chat (no TTS desired) will still:

1. Run the full TTS stage every turn
2. Stream large base64 audio frames
3. Appear “stuck” or fail on clients that only handle text deltas / small WS frames

Happy to help with a PR for the `modalities` → `output_modalities` alias if that approach is acceptable.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `07dc4439aa31c35487fcb77f61e142c2151989d7`.  There
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
{"case_id": "mudler_LocalAI__11103__07dc443",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
