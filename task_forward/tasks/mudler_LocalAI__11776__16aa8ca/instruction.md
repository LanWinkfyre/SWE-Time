# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
`POST /v1/realtime/calls` doesn't accept the OpenAI GA WebRTC request shape (multipart in, `application/sdp` out)

### Summary

`POST /v1/realtime/calls` accepts only a JSON request body and answers with a JSON body. OpenAI's GA endpoint accepts `multipart/form-data` or `application/sdp`, and answers with the SDP as plain text. A client written against the documented OpenAI contract therefore cannot complete the WebRTC handshake with LocalAI — it fails at signaling with `400 sdp is required`.

### What OpenAI's endpoint does

Per the [Realtime WebRTC guide](https://developers.openai.com/api/docs/guides/realtime-webrtc), `POST https://api.openai.com/v1/realtime/calls` accepts two request shapes:

1. **Unified interface** — `multipart/form-data` with two fields:
   - `sdp` — the SDP offer (`application/sdp`)
   - `session` — the session config as JSON, which is where `model` lives, alongside `audio.output.voice`, `instructions`, `turn_detection`, and so on
2. **Ephemeral token** — `Content-Type: application/sdp`, the raw SDP offer as the body

In **both** cases the response is the SDP answer as plain text, fed straight to `pc.setRemoteDescription(answer)`. It is not wrapped in JSON.

### What LocalAI does

`core/http/endpoints/openai/realtime_webrtc.go`:

```go
type RealtimeCallRequest struct {
	SDP   string `json:"sdp"`
	Model string `json:"model"`
	LocalAIAssistant bool `json:"localai_assistant,omitempty"`
}

type RealtimeCallResponse struct {
	SDP       string `json:"sdp"`
	SessionID string `json:"session_id"`
}
```

```go
var req RealtimeCallRequest
if err := c.Bind(&req); err != nil { ... }
if req.SDP == "" {
	return c.JSON(http.StatusBadRequest, map[string]string{"error": "sdp is required"})
}
if req.Model == "" {
	return c.JSON(http.StatusBadRequest, map[string]string{"error": "model is required"})
}
...
return c.JSON(http.StatusCreated, RealtimeCallResponse{SDP: localDesc.SDP, SessionID: sessionID})
```

Three divergences:

1. **Request encoding.** The structs carry only `json` tags, so Echo's binder extracts nothing from a multipart body — every field stays empty and the handler returns `400 sdp is required`. `application/sdp` isn't handled either.
2. **Response encoding.** A GA client reads the response body *as* the SDP answer. LocalAI returns `{"sdp": ..., "session_id": ...}`, so the client hands a JSON document to `setRemoteDescription` and the handshake fails.
3. **Where `model` lives.** LocalAI requires it at the top level. In the multipart flow OpenAI carries it inside the `session` object, so even a client that guessed the JSON shape would have to restructure its session config.

### Reproducing

A real client that hits this: ESP-Brookesia's OpenAI agent (`espressif/brookesia_agent_openai`, v0.8.1), which implements the GA multipart flow in `openai/https_client.c` → `https_post_realtime_call()`. Pointed at a LocalAI instance it gets `400 sdp is required` before any media flows.

By hand:

```sh
# Fails against LocalAI, works against api.openai.com
curl -X POST "$LOCALAI/v1/realtime/calls" \
  -H "Authorization: Bearer $KEY" \
  -F "sdp=<offer.sdp;type=application/sdp" \
  -F 'session={"type":"realtime","model":"my-model"};type=application/json'
# -> {"error":"sdp is required"}
```

### Suggested fix

In `RealtimeCalls()`, branch on the request `Content-Type` before binding:

- `multipart/form-data` — read the `sdp` part as the offer and the `session` part as JSON, taking `model` from inside it (and ideally honouring the rest of the session config: `voice`, `instructions`, `turn_detection`).
- `application/sdp` — the body is the offer; take `model` from the `?model=` query parameter, as the ephemeral-token flow does.
- `application/json` — current behaviour, kept for compatibility.

For the response, return `Content-Type: application/sdp` with the bare answer when the request came in either GA shape, and keep the JSON response for JSON requests. Content negotiation on the request encoding keeps every existing client working while making GA clients work too.

### Why it's worth doing

The whole point of the OpenAI-compatible surface is that clients written for OpenAI work unmodified. Right now every embedded and browser client built on the documented GA WebRTC flow needs a patched fork to reach LocalAI. Accepting the documented shapes removes that.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `16aa8ca0044f2b107173e1c3a0eb3848cf269e4f`.  There
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
{"case_id": "mudler_LocalAI__11776__16aa8ca",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
