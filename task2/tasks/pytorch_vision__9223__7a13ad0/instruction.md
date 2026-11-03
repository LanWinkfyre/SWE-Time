# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
Support removing keypoints outside the image instead of clamping them to the edges

### 🚀 The feature

When keypoints fall outside of the visible area of an image after a transformation such as cropping or rotation, they are currently clamped to one of the edges of the image, i.e., a keypoint at `[-10, 25]` becomes `[0, 25]`. It would be useful to have an option to remove such invisible keypoints instead.

### Motivation, pitch

Often it makes more sense to omit keypoints that are not visible in the image instead of changing their location, which the current clamping mode does.

It would be useful to be able to specify an alternative  `clamping_mode` for `KeyPoints` tensors that does not move them to the image edges but allows them to have coordinates outside of the image. This clamping mode could be combined with a new transformation `SanitizeKeyPoints`, similar to the existing `SanitizeBoundingBoxes`, which removes such invisible keypoints. Keypoints can sometimes have labels associated with them in a separate tensor, which this transformation should be able to remove as well.

### Alternatives

_No response_

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7a13ad0f89167089616b51f4fd07f978cf1f17e4`.  There
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
{"case_id": "pytorch_vision__9223__7a13ad0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
