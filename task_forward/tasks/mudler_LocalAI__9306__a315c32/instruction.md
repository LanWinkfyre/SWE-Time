# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
[whisper] word timings in verbose_json

**Is your feature request related to a problem? Please describe.**
When calling the transcription endpoint with the format `verbose_json`, localai currently only returns a list of segments with `text`, `start` & `end`. The `words` attribute is always None.

**Describe the solution you'd like**
Localai should also provide word level timestamps when requested with `timestamp_granularities=["word"]`

**Describe alternatives you've considered**

**Additional context**
I'm trying to generate subtitles for videos with hardware acceleration (Vulkan). The data returned with format as srt works, but the timestamps are inaccurate. I would like to use [stable-ts](https://github.com/jianfch/stable-ts) to improve the timestamps, but without word level timestamps the results are still suboptimal.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a315c321c188c559c01d0b1b6153c381758ea057`.  There
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
{"case_id": "mudler_LocalAI__9306__a315c32",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
