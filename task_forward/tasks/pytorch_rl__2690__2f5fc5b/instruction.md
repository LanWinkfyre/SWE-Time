# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG]`fps` in `VideoRecorder` Is Undocumented While `video_fps` in `CSVLogger` Is Ineffective

## Describe the bug

When creating videos with `VideoRecorder` and `CSVLogger`, the playback FPS always defaults to 6 FPS—even if `video_fps=30` is specified in `CSVLogger`. After investigating the source code, it appears there is an undocumented `fps` parameter in the `VideoRecorder` constructor that actually controls the playback FPS. Meanwhile, the `video_fps` parameter in `CSVLogger` does not affect the playback FPS, creating confusion and causing users to believe that `video_fps` alone should control the FPS.

## To Reproduce

1. Create a `CSVLogger` specifying `video_fps=30`.
2. Pass this logger to `VideoRecorder`.
3. Record an environment rollout.
4. Observe that the resulting video’s playback rate is still at 6 FPS.

### Minimal Example

```python
from torchrl.record import CSVLogger, VideoRecorder
from torchrl.envs import TransformedEnv
from torchrl.envs import GymEnv

env_factory = lambda **args: GymEnv('LunarLander-v2', **args)

csv_logger = CSVLogger(
    exp_name="example",
    log_dir="./.tmp/",
    video_format="mp4",
    video_fps=30,  # This parameter appears not to affect playback FPS
)
video_recorder = VideoRecorder(
    logger=csv_logger,
    tag="video"
    # fps parameter is missing from documentation, but is needed for correct playback rate
)

record_env = TransformedEnv(env_factory(from_pixels=True, pixels_only=False), video_recorder)
record_env.rollout(max_steps=1000)
video_recorder.dump()
```

### Observed Behavior

- The video plays back at 6 FPS, despite specifying `video_fps=30` in `CSVLogger`.

### Expected Behavior

- Users would expect that setting `video_fps` in `CSVLogger` is sufficient to record and play back the video at the specified FPS.  
- Alternatively, the documentation should clearly indicate that `fps` must be passed to `VideoRecorder` for controlling playback FPS.

## System Info

- **Library Installation**: conda-forge  
- **Python Version**: 3.12.2  
- **torchrl**: 0.6.0  
- **numpy**: 1.26.4  
- **Platform**: Linux  

## Additional Context

- **Documentation Gap**: 
  - The `VideoRecorder` constructor has an `fps` argument, but there is no mention of it in the official documentation.  
  - The `CSVLogger` offers a `video_fps` parameter that does not actually control the playback FPS when using `VideoRecorder`.  

### Working Example

The workaround is to manually specify the `fps` in `VideoRecorder`:

```python
csv_logger = CSVLogger(exp_name="example", log_dir="./.tmp/", video_format="mp4")
video_recorder = VideoRecorder(csv_logger, tag="video", fps=30)
```

## Reason & Possible Fixes

- **Root Cause**: Misleading (or missing) documentation:
  - `video_fps` in `CSVLogger` suggests that it sets the FPS for videos, but it does not.  
  - `fps` in `VideoRecorder` actually controls the video’s playback FPS, but it is undocumented.
- **Proposed Fix**:
  1. Update the `VideoRecorder` [documentation](https://github.com/pytorch/rl/tree/main/docs/) to include and describe the `fps` parameter.  
  2. Clarify in the `CSVLogger` docs that `video_fps` does **not** override the FPS in `VideoRecorder`.  
  3. (Optional) Deprecate or rename `video_fps` in `CSVLogger` if it’s not intended to control playback FPS.

## Checklist

- [x] I have checked that there is no similar issue in the repo  
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/)  
- [x] I have provided a minimal working example to reproduce the bug  

---
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2f5fc5b9e07202d3c4d2eff6be2e7b3d2d7fd02b`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "pytorch_rl__2690__2f5fc5b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
