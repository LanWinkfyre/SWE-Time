# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(security): managed-image OpenClaw security job cannot resolve the built shared boundary

## Investigation Summary

- `managed-image-openclaw-security` fails at test collection with `Error: Cannot find module '../../nemoclaw/dist/shared/sandbox-name.cjs'`.
- The job never builds that artifact. Its steps are Checkout, Set up Node, Install root dependencies, Download image artifact, Load image, then `Validate OpenClaw managed-image security boundary` — there is no build step between dependency install and the test run.
- `nemoclaw/dist/shared/*.cjs` is produced by `npm run build:cli`, whose `build:policy-boundary` step compiles `nemoclaw/tsconfig.shared.json`. That config lists `src/shared/sandbox-name.cts`, so the module builds correctly when the step runs.
- The E2E fixtures import these built artifacts directly, for example `test/e2e/fixtures/gateway-provider-policy-binding.ts` imports `../../../nemoclaw/dist/shared/openshell-policy-boundary.cjs`, so collecting the suite requires the compiled boundary to exist.
- Deterministic, and not specific to one branch: it failed on two consecutive heads of PR #11166 (`9d41a90ad`, `8394519a1`) and also fails on PR #11196.

## Description

The `managed-image-openclaw-security` job installs dependencies and loads a prebuilt image, then runs `test/e2e-runtime/managed-image-openclaw-security.test.ts` without compiling the `nemoclaw` shared boundary. The suite fails during collection because a fixture in its import graph resolves a compiled `.cjs` module that was never produced.

**Expected:** the job either builds the shared boundary before running the suite, or consumes it from an artifact produced by an earlier job.

**Actual:** the suite cannot be collected and the job fails, regardless of the change under test.

This is a job-wiring gap rather than a product defect, but it presents to PR authors as a red security-boundary check on their own change, which makes triage misleading.

## Reproduction Steps

1. Open or update any PR that runs the `Publish complete managed images` workflow.
2. Wait for the `managed-image-openclaw-security` job.
3. The job fails during test collection with the missing-module error.

To confirm the cause locally:

```bash
rm -rf nemoclaw/dist
npx vitest run test/e2e-runtime/managed-image-openclaw-security.test.ts   # missing module
npm run build:cli
ls nemoclaw/dist/shared/sandbox-name.cjs                                  # now present
```

## Environment

- Runner: GitHub-hosted CI, `Publish complete managed images` workflow, job `managed-image-openclaw-security`
- Observed on PR #11166 heads `9d41a90ad` and `8394519a1`, and on PR #11196
- Example run: https://github.com/NVIDIA/NemoClaw/actions/runs/34432328378
- Not host-specific.

## Debug Output

Not applicable. The failure occurs in CI during test collection, before any sandbox exists, so `nemoclaw debug` has nothing to collect. The workflow log and the job step list below are the relevant evidence.

## Logs

```text
FAIL  integration  test/e2e-runtime/managed-image-openclaw-security.test.ts
Error: Cannot find module '../../nemoclaw/dist/shared/sandbox-name.cjs'
Test Files  1 failed (1)
##[error]Process completed with exit code 1.
```

Job step list, showing no build between dependency install and the test run:

```text
success  Install root dependencies
success  Download image artifact
success  Load image
failure  Validate OpenClaw managed-image security boundary
```

## Suggested Fix

Give the job the compiled shared boundary before it runs the suite. Either:

- run the existing build step that produces `nemoclaw/dist/shared/` in this job, or
- publish `nemoclaw/dist/shared/` from the job that already builds it and download it here alongside the image artifact.

Whichever is chosen, a collection-time failure caused by a missing build output should not be reported as a security-boundary result, because it is indistinguishable from a real posture regression in the PR under review.

Related: #10979.

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2c3761bc0d68bc1953ed1eddce7a61057c01b384`.  There
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
{"case_id": "NVIDIA_NemoClaw__11368__2c3761b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
