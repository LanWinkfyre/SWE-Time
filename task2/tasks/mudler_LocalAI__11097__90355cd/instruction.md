# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
omnivoice-cpp backend: `speed` parameter is silently ignored in /v1/audio/speech

## Bug: `speed` parameter is silently ignored by the `omnivoice-cpp` TTS backend

### Environment
- LocalAI version: `v4.7.1` (`b224c96db6f4b87306a33a808650bfce63b12588`)
- Image: `localai/localai:latest-gpu-nvidia-cuda-13`
- Backend: `omnivoice-cpp` (also reproduces on `omnivoice-cpp-hq`)
- Model config:
  ```yaml
  backend: omnivoice-cpp
  name: omnivoice-cpp
  options:
      - tokenizer:omnivoice-tokenizer-Q8_0.gguf
  parameters:
      model: omnivoice-cpp/omnivoice-base-Q8_0.gguf
  tts:
      voice_cloning: true
  ```
- Voice: a cloned profile from the Voice Library (`localai://voice-profiles/{uuid}`), but reproduces with any voice.

### Steps to reproduce
Two requests, identical except for `speed`:

```bash
curl -s https://<localai>/v1/audio/speech \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "omnivoice-cpp",
    "input": "The quick brown fox jumps over the lazy dog.",
    "voice": "localai://voice-profiles/<uuid>",
    "response_format": "wav",
    "speed": 1.0
  }' -o speed_1_0.wav

curl -s https://<localai>/v1/audio/speech \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "omnivoice-cpp",
    "input": "The quick brown fox jumps over the lazy dog.",
    "voice": "localai://voice-profiles/<uuid>",
    "response_format": "wav",
    "speed": 0.8
  }' -o speed_0_8.wav
```

### Expected behavior
`speed=0.8` should produce a proportionally longer/slower clip than `speed=1.0` (per the OpenAI TTS API contract LocalAI's `/v1/audio/speech` is compatible with — `speed` is a documented request field, range 0.25–4.0).

### Actual behavior
Both requests return byte-identical-length audio:

```
speed=1.0 -> duration 2.32s
speed=0.8 -> duration 2.32s   (unchanged)
```

The request succeeds (HTTP 200, no error), so the parameter is silently dropped rather than rejected — it just has no effect, which makes the bug easy to miss.

### Comparison / sanity check
Ran the identical request (same text, same underlying model/voice) against a different OpenAI-compatible TTS server also wrapping an OmniVoice-family model, which honors `speed` correctly:

```
speed=1.0 -> duration 2.32s
speed=0.8 -> duration 2.84s   (~1.22x longer, as expected)
```

So this looks specific to the LocalAI `omnivoice-cpp` backend's request handling (or the omnivoice-cpp gRPC backend itself not implementing the `speed`/rate parameter), not a client-side or model-capability issue.

### Additional context
Other TTS-request parameters on this backend work as documented in the same test pass:
- Voice cloning via `localai://voice-profiles/{uuid}` — works, output duration matches a reference implementation closely (within ~0.1s across 7 different voices).
- `instructions` (voice-design keywords, e.g. `"male, low pitch"`) — works.
- `instructions` with free-form natural-language text (not from the documented keyword vocabulary) — returns `500 Internal Server Error: "omnivoice: synthesis failed"` rather than a validation error naming the allowed vocabulary. Worth a friendlier 400 here too, filing as a side note rather than the main bug.

Happy to provide the full test script / raw WAV files if useful.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `90355cd44420e0cdbd9b79d7ce763341990a6851`.  There
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
{"case_id": "mudler_LocalAI__11097__90355cd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
