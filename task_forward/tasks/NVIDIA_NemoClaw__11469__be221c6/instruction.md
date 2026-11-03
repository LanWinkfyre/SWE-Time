# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Linux][Upgrade] strict pre-upgrade backup abort leaves a partial timestamp directory

## Description

NemoClaw v0.0.122 correctly aborts a strict pre-upgrade backup when a registered running sandbox is unreachable, but it still creates a new timestamped backup directory. The directory is incomplete and can be mistaken for a usable recovery point.

The same behavior was reproduced independently on Ubuntu 22.04 and Ubuntu 26.04. The installer exits nonzero as required; the defect is the new partial backup artifact left behind after the abort.

- Platform scope: Ubuntu 22.04 and Ubuntu 26.04 x86_64
- Regression: Unknown; earlier releases were not tested for this exact artifact behavior
- OpenShell issue: No. NemoClaw owns the pre-upgrade backup transaction and directory cleanup

## Environment

```text
Device:        Generic Ubuntu hosts
OS:            Ubuntu 22.04 and Ubuntu 26.04
Architecture:  x86_64
Node.js:       v22.22.3 on Ubuntu 22.04; v22.23.1 on Ubuntu 26.04
npm:           10.9.8
Docker:        29.4.0 on Ubuntu 22.04; 29.6.1 on Ubuntu 26.04
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.122
OpenClaw:      2026.7.1
Agent:         OpenClaw
```

## Steps to reproduce

1. Install NemoClaw v0.0.122 and onboard an OpenClaw sandbox.
2. Confirm the sandbox is recorded as running and list the existing timestamped directories under the NemoClaw backup root.
3. Make the sandbox runtime unreachable while leaving its registered running state intact.
4. Run the v0.0.122 installer again using the default strict pre-upgrade backup behavior.
5. Confirm that the installer aborts, then list the backup root again.

## Expected result

The installer exits nonzero with an actionable message because the running sandbox cannot be backed up. The backup operation is transactional: no new timestamped directory or other partial recovery artifact remains after the failed backup.

## Actual result

The installer exits nonzero, but a new timestamped backup directory remains on both tested Ubuntu releases.

```text
Ubuntu 22.04:
  before: one existing timestamped directory
  after:  the existing directory plus one newly created directory

Ubuntu 26.04:
  before: one existing timestamped directory
  after:  the existing directory plus one newly created directory
```

The new directory is created by the failed strict backup attempt and is not a trustworthy recovery point.

## Logs

```text
Strict pre-upgrade backup begins for a registered running sandbox.
The sandbox connection fails as intentionally arranged for the negative test.
The installer reports that the backup failed and exits nonzero.
A fresh timestamped directory is nevertheless present in the backup root after the command returns.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `be221c6307959a86c04ad16974b6ef970bc9b613`.  There
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
{"case_id": "NVIDIA_NemoClaw__11469__be221c6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
