# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
liquid-audio backend: AudioTransformStream RPC raises NotImplementedError (realtime streaming never works, on any hardware)

## Environment
- LocalAI v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588)
- Backend image: `rocm-liquid-audio` (quay.io/go-skynet/local-ai-backends, latest-gpu-rocm-hipblas-liquid-audio)
- Model: `LiquidAI/LFM2.5-Audio-1.5B`, `mode:s2s`
- Note: this does not look GPU-vendor specific - the RPC method itself is unimplemented in the Python backend, so this should reproduce identically on CUDA/CPU builds too.

## What happened
The model is tagged `speech-to-speech`/`any-to-any`/`realtime`, and its gallery description says it "is the model the LocalAI realtime API any-to-any path consumes." Loading the model and calling the documented realtime endpoint (`GET /audio/transformations/stream`, WebSocket) gets past the handshake and the `session.update` envelope validation cleanly, but fails as soon as the server forwards the session to the backend:

Client side:
```json
{"type":"error","error":"backend send config: EOF"}
```

Backend log:
```
Liquid-audio mode=s2s, voice=us_female
ERROR:grpc._server:Exception calling application: Method not implemented!
Traceback (most recent call last):
  File ".../venv/lib/python3.12/site-packages/grpc/_server.py", line 608, in _call_behavior
    response_or_iterator = behavior(argument, context)
  File ".../rocm-liquid-audio/backend_pb2_grpc.py", line 571, in AudioTransformStream
    raise NotImplementedError('Method not implemented!')
NotImplementedError: Method not implemented!
```

## Reproduction
1. Register `lfm2.5-audio-1.5b-realtime` (backend `liquid-audio`, `model: LiquidAI/LFM2.5-Audio-1.5B`, `options: [mode:s2s]`).
2. `POST /backend/load {"model": "lfm2.5-audio-1.5b-realtime"}` - succeeds, model loads fine.
3. Open `GET /audio/transformations/stream` over WebSocket, send `{"type":"session.update","model":"lfm2.5-audio-1.5b-realtime","input_audio_format":"pcm16","output_audio_format":"pcm16","sample_rate":16000}`.
4. Server replies `{"type":"error","error":"backend send config: EOF"}` - the backend process has crashed the RPC handler with the traceback above.

## Note on session.update format, since it's undocumented
The Swagger doc gives no schema for this WebSocket's first message beyond prose ("JSON `session.update` envelope describing model + sample format + frame size + backend params"). For anyone else hitting this: `model` must be a **top-level** key on the envelope, not nested under a `session` object - sending it nested gets `{"type":"error","error":"session.update missing model"}`. Might be worth documenting this in the Swagger/docs regardless of the NotImplementedError above.

## Expected
Either `AudioTransformStream` gets a real implementation in the `liquid-audio` backend, or the model/backend shouldn't be tagged `realtime`/`speech-to-speech` streaming if that path is known-unimplemented - the tagging is what led to registering it as the any-to-any realtime option in the first place.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c29c99e120cdd169b35c57e754126a4b85aa5fb4`.  There
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
{"case_id": "mudler_LocalAI__11564__c29c99e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
