# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Linux][Docs] Hermes recovery page links to an OpenClaw recover anchor

## Description

The published Hermes recovery page links to the Hermes Commands page with the fragment `nemoclaw-name-recover`. That fragment is absent; the Hermes command heading uses `nemohermes-name-recover`.

Platform scope: Reproduced on Linux only; other platforms not tested

Regression: Unknown — earlier published documentation versions not tested

OpenShell issue: No

## Environment

```text
Device:        Documentation validation host
OS:            Ubuntu 24.04
Architecture:  x86_64
Node.js:       N/A — published documentation validation only
npm:           N/A — published documentation validation only
Docker:        N/A — published documentation validation only
OpenShell CLI: N/A — published documentation validation only
NemoClaw:      v0.0.119 documentation
OpenClaw:      N/A — published documentation validation only
```

## Steps to Reproduce

1. Open https://docs.nvidia.com/nemoclaw/user-guide/hermes/manage-sandboxes/operate-sandboxes/recover-and-rebuild-sandboxes.
2. Follow the recover command reference link in the portable Hermes recovery guidance.
3. Observe that the browser opens the Hermes Commands page with the `nemoclaw-name-recover` fragment.
4. Observe that no heading uses that fragment.
5. Navigate to the `nemohermes-name-recover` fragment and observe that the intended recover command section exists there.

## Expected Result

The recovery page links to the `nemohermes-name-recover` section on the Hermes Commands page.

## Actual Result

The link uses `nemoclaw-name-recover`, so the Commands page opens without navigating to the intended Hermes recover section.

## Logs

```text
Recovery-page fragment: nemoclaw-name-recover
Hermes Commands target count for nemoclaw-name-recover: 0
Hermes Commands target count for nemohermes-name-recover: 1
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5150eb77b06d50526c293bd7f22ea67f85b64215`.  There
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
{"case_id": "NVIDIA_NemoClaw__11147__5150eb7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
