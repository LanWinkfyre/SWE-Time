# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Station][Install] documented install command downgrades a newer host to the lkg tag and leaves it unable to run any sandbox command

## Description

Running the documented install command on a host whose NemoClaw is newer than the installer's
maintained "lkg" tag silently downgrades that host, and the aborted run leaves it unusable.

The installer resolves its install ref to "lkg" without comparing it to the version already
present. On a host running v0.0.119 it installed v0.0.109. It swaps the CLI first and only then
runs the pre-upgrade backup, which the older CLI cannot complete because it cannot read a
registry entry written by the newer one. The installer stops at that point, and the host is left
on the older CLI where every sandbox command fails with the same error.

Recovery requires knowing to pin the tag explicitly, which the documented command does not
mention.

There is a fixed issue for the same root cause on a different entry point: the update command
was given a downgrade guard. That guard does not cover this installer path, and the outcome here
is worse: the earlier report ended in a misleading message, while this one ends with the host
unable to run any sandbox command.

Platform scope: Reproduced on DGX Station GB300 aarch64; other platforms not tested for this
                path, but the version comparison is performed by the shared installer script.
Regression: Unknown - earlier releases were not tested for this path.
OpenShell issue: No. The failing step is NemoClaw's own installer.

## Environment

```text
Device:        NVIDIA DGX Station GB300
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.1
Docker:        Docker version 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.119 before the command, v0.0.109 after it
```

## Steps to Reproduce

```bash
1. Start from a host running a NemoClaw release newer than the current maintained "lkg" tag, with
   at least one registered sandbox created by that newer release. Record the starting version:
     nemoclaw --version

2. Run the install command exactly as the documentation gives it:
     curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash

3. Record the exit code and the version afterwards:
     nemoclaw --version

4. Try any sandbox command:
     nemoclaw list
     nemoclaw {sandbox} recover
```

## Expected Result

The installer compares the maintained tag with the installed version and refuses to replace a
newer install with an older one, or warns clearly and requires explicit confirmation. It does
not leave the host on a CLI that cannot read its own registry.

## Actual Result

The version goes backwards and the host stops working.

  before:  nemoclaw v0.0.119
  after:   nemoclaw v0.0.109

The installer log shows it never considered the installed version:

  [INFO]  Resolved install ref: lkg

It swaps the CLI before validating, then fails during the pre-upgrade backup:

  [INFO]  Deferring OpenShell CLI installation until after pre-upgrade backup.
  [INFO]  Verified: nemoclaw is available at {path}/nemoclaw
  Error: Cannot load a sandbox entry with an invalid workload receipt
  [ERROR] Pre-upgrade backup stopped the installer. Resolve every reported sandbox backup
          failure or skipped sandbox using the CLI output above, then rerun the installer.

After that, every sandbox command fails the same way, so the guidance to "rerun the installer"
cannot succeed either:

  nemoclaw list                     fails with: Cannot load a sandbox entry with an invalid workload receipt
  nemoclaw {sandbox} recover        fails with: Cannot load a sandbox entry with an invalid workload receipt
  nemoclaw {sandbox} dashboard-url  fails with: Cannot load a sandbox entry with an invalid workload receipt

The registry entry it cannot read was written by the newer release and carries no workload
receipt field at all.

The host was recovered only by rerunning the installer with the tag pinned to the newer release,
which is not part of the documented command.

## Logs

```text
Installer, in order:

  [INFO]  Resolved install ref: lkg
  [INFO]  Deferring OpenShell CLI installation until after pre-upgrade backup.
  [INFO]  Verified: nemoclaw is available at {path}/nemoclaw
  Error: Cannot load a sandbox entry with an invalid workload receipt
  [ERROR] Pre-upgrade backup stopped the installer.
```

## Related issues / not duplicate of

- **#8306** — same root cause (the fixed `lkg` tag can be older than the installed build, with no downgrade guard) but on the `nemoclaw update --fresh` entry point, and closed as completed. The guard added there does not cover the installer path documented for end users, and the outcome here is more severe: the host is left unable to run any sandbox command rather than just printing a misleading message.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `801fb0c5bad751d4c06fdd51840bf5e755b5a48c`.  There
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
{"case_id": "NVIDIA_NemoClaw__11160__801fb0c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
