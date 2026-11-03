# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
WhisperX diarization fails becuase it calls non-existing function

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
<!-- Container Image or LocalAI tag/commit -->
localai/localai:latest 
sha256:d62ab7bb1c578febf2a4ea2566c294d5f334bdd822e48a896ee10cca950ec177

quay.io/go-skynet/local-ai-backends:latest-cpu-whisperx
sha256:6fe6048b90aa0e5ba50ec42733037de1b95ceb49b9524ee71f1176c4f069421b

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
When you call the Audio Transcription API, and have selected to do diarization as part of the transcription, it fails and returns HTTP status code `200` and a Json object with an empty "text" property.

In the Backend log you will find the error

```
Unexpected err=AttributeError("module 'whisperx' has no attribute 'DiarizationPipeline'"), type(err)=<class 'AttributeError'>
```

This error occurs because it tries to create the diarization pipeline with this

```python
    self.diarize_pipeline = whisperx.DiarizationPipeline(
        use_auth_token=self.hf_token,
        device=self.device,
    )
```

But since WhisperX 3.6.0 it should be done like this

```python
    self.diarize_pipeline = DiarizationPipeline(
        token=self.hf_token,
        device=self.device,
    )
```

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->

1. Install the `WhisperX` backend.
2. Create a new model using the following yaml:

```yaml
backend: whisperx
description: WhisperX 
known_usecases:
    - transcript
    - diarization
name: kb-whisper-base
parameters:
    model: KBLab/kb-whisper-base
```
3. Download the audio file https://cdn.openai.com/whisper/draft-20220913a/micro-machines.wav
4. Call the Transcription API
```bash
curl -X 'POST' \
  'http://localhost:8080/v1/audio/transcriptions' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'model=kb-whisper-base-x' \
  -F 'diarize=true' \
  -F 'file=[PATH]/micro-machines.wav;type=audio/wav'
```

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
A json file returned with a transcription and diarization of the audio file.

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c4cd86bb156e52c146a0572db30e7d622c89f743`.  There
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
{"case_id": "mudler_LocalAI__10388__c4cd86b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
