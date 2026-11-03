# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Shasum error installing audio-cpp-sortformer-diarization

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
4.8.2
**Environment, CPU architecture, OS, and Version:**
Macbook air m4. MacOS 27 beta5. 

**Describe the bug**
Sha mismatch. Couldn't install model
audio-cpp-sortformer-diarization
·
SHA mismatch for file "/Users/user/.localai/models/audio-cpp/sortformer-diar-4spk-v1-q8_0.gguf" ( calculated: 4fa6a3e30c4a1c6cc1da455268806edc9343...

**To Reproduce**
Maybe other have same if downloable model has been updated?
**Expected behavior**
Click install. Wait for download and sha check verification and installation.
**Logs**
App does not provide log to terminal.

**Additional context**
Thanks for this app. It looks just what i needed.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `88edd7fc7f713b54735ab46c8cd3b99dfae4630d`.  There
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
{"case_id": "mudler_LocalAI__11534__88edd7f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
