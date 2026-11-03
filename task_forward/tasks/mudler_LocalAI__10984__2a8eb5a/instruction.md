# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Realtime Voice pipeline is broken: undocumented Opus installation workflow and kokoro / kokoros backend mismatch

Environment
LocalAI v4.7.1
Docker (localai/localai:latest)
Debian 13
CPU only
Clean installation
Realtime Talk enabled
Summary

While configuring Realtime Talk on a clean installation, I encountered two consecutive issues that prevent the voice pipeline from working.

The first issue prevents the Opus backend from being installed using the expected workflow.

After discovering a manual workaround and successfully installing Opus, Realtime progresses further but immediately fails because the TTS pipeline requests a backend named kokoro, while the installed backend is named kokoros.

These appear to be two bugs in the same Realtime Voice pipeline.

Issue 1 - Opus backend cannot be installed using the expected workflow

Initially, Realtime failed with:

backend not found: opus

Trying to install Opus through the models API did not work.

POST /models/apply
{
  "id":"opus"
}

The backend was never installed.

The only method that worked was:

curl http://localhost:8080/backends/apply \
-H "Content-Type: application/json" \
-d '{"id":"opus"}'

After that:

/backends/opus
/backends/cpu-opus

were correctly installed and the original Opus error disappeared.

At this point Realtime started creating sessions successfully.

Issue 2 - TTS backend name mismatch

After fixing Opus, Realtime no longer failed during session creation.

Instead it failed during TTS warm-up:

ERROR realtime warmup failed

tts (kokoro):

backend not found: kokoro

The configured pipeline is:

{
  "name":"argos-voice",
  "vad":"silero-vad",
  "transcription":"whisper-small",
  "llm":"qwen3-4b",
  "tts":"kokoro",
  "voice":"argos-voice"
}

However the installed backend list contains only:

cpu-kokoros
kokoros

There is no backend named:

kokoro

The backend gallery also reports:

alias: kokoros
installed: true

Therefore the pipeline requests:

kokoro

while the installed backend is:

kokoros

which results in:

backend not found: kokoro
Result

Current behavior:

Realtime initially fails because Opus cannot be installed using the expected workflow.
After manually installing Opus through /backends/apply, Realtime successfully creates the voice session.
During warm-up, the TTS initialization fails because the pipeline requests kokoro while the installed backend is kokoros.
Talk shows Connecting... for a few seconds and then disconnects.

As a result, Realtime Voice cannot be used on a clean installation.

Expected behavior
Opus should be installable using the documented workflow.
The TTS pipeline should reference the correct backend name, or a compatibility alias should exist (kokoro ↔ kokoros), so that the installed backend can be loaded correctly.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2a8eb5a04b04822de8d83d7a5335c36947fbffc5`.  There
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
{"case_id": "mudler_LocalAI__10984__2a8eb5a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
