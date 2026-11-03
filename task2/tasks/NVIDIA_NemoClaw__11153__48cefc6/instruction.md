# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][DGX Station][Upgrade] installer reports the sandbox upgrade unfinished and exits 1 while the rebuilt sandbox is healthy

## Description

Upgrading a host that has one pre-existing sandbox needing an image upgrade ends with the
installer declaring the upgrade unfinished and exiting 1, while the sandbox it just rebuilt is
in fact healthy. The installer reports that the prepared backup recovery "completed with
unverified post-restore state" and prints recovery instructions, but the sandbox is Ready, its
gateway is running, and its dashboard serves content immediately afterwards with no repair
performed by the tester.

The same installer command on the same host exits 0 when no sandbox needs an image upgrade, so
the false failure is specific to the upgrade-with-recreate path.

A user following the printed guidance would run recovery steps that are not needed, and any
automation gating on the installer exit code treats a successful upgrade as a failed one.

Platform scope: Reproduced independently on two different aarch64 systems, a DGX Station GB300
                and a DGX Spark; x86_64 not tested for this path.
Regression: Unknown - earlier releases were not tested for this path.
OpenShell issue: No. The failing step is NemoClaw's own installer sandbox-upgrade stage.

## Environment

```text
Device:        NVIDIA DGX Station GB300 and NVIDIA DGX Spark
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.1
Docker:        Docker version 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      upgraded from v0.0.119 to v0.0.120
Agent runtime: NemoHermes (Hermes Agent v0.19.0 to v0.20.6)
```

## Steps to Reproduce

```bash
1. On a host running NemoClaw v0.0.119, onboard a NemoHermes sandbox and confirm it is Ready:
     nemoclaw onboard --agent hermes --name {sandbox} --fresh --yes --no-gpu
     nemoclaw {sandbox} status

2. Run the installer pinned to the newer release so the pre-existing sandbox needs an image
   upgrade, and record its exit code:
     curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.120 bash

3. Immediately afterwards, without performing any of the printed recovery steps, check the
   sandbox:
     nemoclaw {sandbox} recover
     nemoclaw {sandbox} dashboard-url --quiet

4. Fetch the dashboard URL captured in step 3 and check the response size.

5. Re-run the same installer command once more, now that the sandbox is already at the new
   version, and record its exit code again.
```

## Expected Result

The installer either completes the sandbox upgrade and exits 0, or, if the post-restore state
genuinely cannot be verified, leaves the sandbox in a state that actually requires the recovery
it prints. The exit code and the sandbox's real condition agree.

## Actual Result

Step 2 exits 1 and prints:

  Failed to recover {sandbox}: Prepared backup recovery for {sandbox} completed with
  unverified post-restore state.
  One or more existing sandboxes could not be recovered automatically.
  Installation incomplete: one or more existing sandboxes failed to upgrade.

Step 3, run immediately and with no repair performed, contradicts that:

  Probe complete: Hermes Agent gateway is running in {sandbox}; restored dashboard port forward.
  ... forwardAction=restored result=ready
  exit code 0

Step 4 fetches the dashboard successfully and receives 1719 bytes.

Step 5, with nothing left to upgrade, exits 0. Only the run that had to recreate the sandbox
for the image upgrade reports the false failure.

The same failure text appeared on a second, different aarch64 system during an independent
v0.0.119 to v0.0.120 upgrade of a NemoHermes sandbox, so it is not specific to one host.

## Logs

```text
Installer, upgrade stage:

  Recovering and upgrading pre-existing sandboxes before onboarding
    {sandbox}  v0.19.0 to v0.20.6; NemoClaw image v0.0.119 to v0.0.120  (running)
  Prepared backup recovery:
    {sandbox}  {timestamp}  (pre-upgrade backup)
  Creating sandbox {sandbox} (this takes a few minutes on first run)...
  Sandbox {sandbox} created
  Failed to recover {sandbox}: Prepared backup recovery for {sandbox} completed with
  unverified post-restore state.
```

## Related issues / not duplicate of

- **#5801** — rebuild/upgrade: atomic build-verify-swap before deleting the old sandbox. Same area of the upgrade flow, but that issue is about deletion ordering; this report is about the exit code and the printed diagnostic contradicting the sandbox's real condition.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48cefc6f53bc158fae59ee319718fc00345f660a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11153__48cefc6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
