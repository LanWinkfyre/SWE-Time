# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Sandbox] rebuild exits 1 and leaves the sandbox in Error phase after its container is killed

## Description

After a sandbox container is killed, `nemoclaw <sandbox> rebuild --yes` exits 1 and leaves the sandbox in `Phase: Error` instead of recreating it. The command reports that it retained an incomplete snapshot for manual recovery, so the documented recovery path for an unhealthy sandbox does not complete and the operator is left with a broken sandbox.

The same command on the same host against a healthy sandbox succeeds and returns Ready, so the failure is specific to the unhealthy state that rebuild exists to repair.

- **Platform scope:** Reproduced on Ubuntu 24.04 x86_64; other platforms not tested by this run.
- **Regression:** Unknown — earlier releases were not tested for this path.
- **OpenShell issue:** No. The failing command is NemoClaw's own rebuild command.

## Environment

```text
Device:        Ubuntu 24.04 x86_64 workstation with an NVIDIA GeForce RTX 5090 D
OS:            Ubuntu 24.04.4 LTS
Architecture:  x86_64
Kernel:        6.17.0-23-generic
Node.js:       v22.23.0
npm:           10.9.8
Docker:        Docker version 29.7.2, build a7dcaa6
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.118
OpenClaw:      not captured
```

## Steps to Reproduce

1. Onboard a sandbox and let it reach Ready. Onboarding exits 0.

   ```bash
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_YES=1 NEMOCLAW_PROVIDER=build \
     nemoclaw onboard --name <sandbox> --yes
   ```

2. Write a marker file inside the sandbox so state preservation can be checked later.

   ```bash
   nemoclaw <sandbox> exec -- sh -c 'echo marker > /sandbox/.openclaw/workspace/txn-marker.txt'
   ```

3. Force the container into an unhealthy state. `docker kill` exits 0.

   ```bash
   docker kill <container id of that sandbox>
   ```

4. Run the documented recovery.

   ```bash
   nemoclaw <sandbox> rebuild --yes
   ```

5. Ask for the sandbox state.

   ```bash
   nemoclaw <sandbox> status
   ```

6. Control, on the same host: onboard a second sandbox, leave it healthy, and rebuild it.

   ```bash
   nemoclaw <other sandbox> rebuild --yes
   ```

## Expected Result

Step 4 exits 0. The output shows state backup before recreation, successful recreation and an identity-pinned restore, with no error or rollback message. Step 5 reports the sandbox Ready and exits 0, and the marker file written in step 2 is still present.

## Actual Result

Step 4 exits 1, ending with an incomplete-snapshot notice. Step 5 reports `Phase: Error` and exits 1. No running container exists for the sandbox afterwards, so the marker file and the managed file modes cannot be checked at all.

Step 6, the control on the same host minutes later, exits 0 and the control sandbox reports `Phase: Ready`. The host is therefore capable of a successful rebuild; only the post-kill path fails.

## Logs

```text
rebuild exit code: 1
  Incomplete snapshot retained for manual recovery:
  <home>/.nemoclaw/rebuild-backups/<sandbox>/2026-09-04T10-48-51-015Z
  It is excluded from snapshot restore selection.

status exit code: 1
  Phase: Error

follow-up exec:
  OpenClaw permission cleanup failed (command exit 1; cleanup exit 1): No running direct OpenShell
  sandbox container found for '<sandbox>' (driver: docker). Expected one OpenShell-managed container
  labeled 'openshell.ai/sandbox-name=<sandbox>' and named openshell-<sandbox>,
  openshell-<sandbox>-*, or openshell-default--<sandbox>-*. Is the sandbox running?

control sandbox, same host:
  rebuild exit code: 0
  status exit code: 0, Phase: Ready
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `133a1886c318a45adc0a979cc1e6ebfc407bf066`.  There
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
{"case_id": "NVIDIA_NemoClaw__11137__133a188",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
