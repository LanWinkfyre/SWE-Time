# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
qwen-asr: wrong handling of language ("de" vs "German")

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
LocalAI v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588)
<!-- Container Image or LocalAI tag/commit -->

**Environment, CPU architecture, OS, and Version:**
Ryzen 5700G iGPU via Vulkan in Docker
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->

**Describe the bug**
I think the language handling for qwen-asr in backend.py is wrong:
If I set parameters.language to "German", everything works. If I set it to "de", I get the following stack trace.
In theory, I would be fine with just setting "German", BUT: most third-party software will request the API with language="de", and therefore doesn't work at all (e.g. Homeassistant via wyoming_openai).
I think proper mapping is needed for language codes -> language name that qwen-asr understands.

```
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="Error in AudioTranscription: Unsupported language: De. Supported: ['Chinese', 'English', 'Cantonese', 'Arabic', 'German', 'French', 'Spanish', 'Portuguese', 'Indonesian', 'Italian', 'Korean', 'Russian', 'Thai', 'Vietnamese', 'Japanese', 'Turkish', 'Hindi', 'Malay', 'Dutch', 'Swedish', 'Danish', 'Finnish', 'Polish', 'Czech', 'Filipino', 'Persian', 'Greek', 'Romanian', 'Hungarian', 'Macedonian']" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="Traceback (most recent call last):" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="  File \"/backends/cpu-qwen-asr/backend.py\", line 310, in AudioTranscription" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="    results = self.model.transcribe(" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="              ^^^^^^^^^^^^^^^^^^^^^^" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="  File \"/backends/cpu-qwen-asr/venv/lib/python3.12/site-packages/torch/utils/_contextlib.py\", line 124, in decorate_context" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG Transcribed transcription=&{[] []   0 false} caller={caller.file="/build/core/http/endpoints/openai/transcription.go"  caller.L=175 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="    return func(*args, **kwargs)" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="           ^^^^^^^^^^^^^^^^^^^^^" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="  File \"/backends/cpu-qwen-asr/venv/lib/python3.12/site-packages/qwen_asr/inference/qwen3_asr.py\", line 363, in transcribe" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="    validate_language(ln)" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="  File \"/backends/cpu-qwen-asr/venv/lib/python3.12/site-packages/qwen_asr/inference/utils.py\", line 106, in validate_language" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="    raise ValueError(f\"Unsupported language: {language}. Supported: {SUPPORTED_LANGUAGES}\")" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
DEBUG GRPC stderr id="qwen3-asr-0.6b-127.0.0.1:36221" line="ValueError: Unsupported language: De. Supported: ['Chinese', 'English', 'Cantonese', 'Arabic', 'German', 'French', 'Spanish', 'Portuguese', 'Indonesian', 'Italian', 'Korean', 'Russian', 'Thai', 'Vietnamese', 'Japanese', 'Turkish', 'Hindi', 'Malay', 'Dutch', 'Swedish', 'Danish', 'Finnish', 'Polish', 'Czech', 'Filipino', 'Persian', 'Greek', 'Romanian', 'Hungarian', 'Macedonian']" caller={caller.file="/build/pkg/model/process.go"  caller.L=219 } 
```

<!-- A clear and concise description of what the bug is. -->

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->
Set language.parameters to "de" for qwen3-asr-0.6b

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
Proper STT without stack trace

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->
see above

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0e0221b0f51be2aa2c7ac9b6d3898bbed1a87638`.  There
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
{"case_id": "mudler_LocalAI__10958__0e0221b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
