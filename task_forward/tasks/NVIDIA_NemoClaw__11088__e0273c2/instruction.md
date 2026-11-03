# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(npm): protected OpenClaw image build exhausts audit completeness retries

## Investigation Summary

- The [PR #11071 E2E run](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523) tested candidate `0ddc3ea52efe8a5d63099b92f43cbe0a43c88a01` through trusted workflow commit `4b254b9bef3e0ba745af4859fc65700742f5317e`.
- [Protected managed-image GPU and local inference](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101169742484) failed while building the OpenClaw protected image.
- The reviewed mcporter audit reported `incomplete-report`, retried once after one second, and remained incomplete after two attempts.
- The image build then exited 1 before protected runtime inference ran.
- This is not a downstream aggregate failure and is separate from the receipt-identity mismatch fixed by merged #11069.

## Description


The protected OpenClaw image build requires a complete reviewed npm audit result. The audit service or parser returned an incomplete report on both bounded attempts, so the build correctly failed closed but did not preserve enough classification to decide whether this was registry instability or a deterministic response-shape regression.

Expected: the reviewed audit returns a complete report, or the job records a precise external or parser failure classification.

Actual: both attempts end with `reason=incomplete-report`, and the protected image is not built.

## Acceptance Criteria

- Preserve a redacted diagnostic identifying which required audit response fields were absent or invalid.
- Distinguish a transient registry/audit response from a deterministic parser or npm-version regression.
- Keep the image build fail-closed when a complete audit cannot be established.
- Use a bounded retry policy and report its final classification.
- The protected managed-image GPU and local-inference job reaches runtime qualification on the fixing commit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e0273c244c0e96ab35bd1d3c962c3802633d67e7`.  There
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
{"case_id": "NVIDIA_NemoClaw__11088__e0273c2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
