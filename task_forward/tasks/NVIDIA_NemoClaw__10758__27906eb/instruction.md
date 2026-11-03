# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Station][Sandbox] rebuild cannot restore provider snapshot acceleration state

## Description

On DGX Station, rebuilding a healthy GPU-enabled OpenClaw sandbox reaches runtime Ready but fails while restoring managed provider snapshot authority. The rebuild exits non-zero and leaves state recovery incomplete because the recreated sandbox cannot represent the saved snapshot acceleration state.

Platform scope: Platform-specific: fails on DGX Station; the equivalent rebuild stage was verified to complete on Ubuntu 22.04 x86_64 and Ubuntu 26.04 x86_64 with NemoClaw v0.0.117.

Regression: Unknown — earlier versions were not tested with this acceleration-state restore path.

OpenShell issue: No — the failure is raised by NemoClaw's managed provider snapshot restore validation after the sandbox reaches Ready.

## Environment

```text
Device:        DGX Station GB300
OS:            Ubuntu 24.04 (Linux 6.17.0-1029-nvidia-64k)
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker Engine 29.6.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. Install NemoClaw v0.0.117 on a DGX Station and onboard a GPU-enabled OpenClaw sandbox named `restore-test`.
2. Register a Slack channel on the sandbox with valid bot and app credentials:

   ```bash
   nemoclaw restore-test channels add slack
   ```

3. Rebuild the sandbox:

   ```bash
   nemoclaw restore-test rebuild --yes
   ```

4. Observe the restore phase after the replacement sandbox reaches Ready.

## Expected Result

The rebuilt sandbox restores its managed provider snapshot authority, preserves its acceleration configuration, returns to Ready, and the rebuild command exits 0.

## Actual Result

The replacement sandbox reaches Ready, but provider snapshot restoration is blocked. The rebuild exits 1, retains the backup, and reports that state recovery remains incomplete.

## Logs

```text
Restoring workspace state...
Restore blocked: Cannot restore provider snapshot authority: Runtime snapshot provider failed: sandbox 'restore-test' cannot represent the snapshot acceleration state.
Partial restore: none
State recovery remains incomplete. Correct the restore error, then run `nemoclaw restore-test rebuild` again.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `27906ebe2abda0c349dadffc13169cfa63e5f256`.  There
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
{"case_id": "NVIDIA_NemoClaw__10758__27906eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
