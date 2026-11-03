# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][CLI&UX] Live onboarding-lock contention reports a bare internal error instead of the shipped "another run is already in progress" guidance

## Description

When a second NemoClaw command runs while a first one genuinely holds the onboarding lock, the second command exits with a bare internal error and no guidance. The product already ships the correct message for exactly this situation — it names the contention, prints the holder PID, and tells the user to wait — but that text is never reached.

Observed on three hosts with three different commands:

```text
onboard started during an onboard   → Cannot update onboarding recovery while another onboarding run owns the lock.
rebuild started during an onboard   → Cannot update onboarding recovery while another onboarding run owns the lock.
uninstall started during an install → Failed to acquire lock on <home>/.nemoclaw-portable-host.lock after 120 retries
```

None of these name the competing run, none print a holder PID, and none say to wait and retry. The shipped guard text that should appear reads:

```text
another nemoclaw onboarding run is already in progress.
Lock holder PID: <pid>
Wait for the active onboarding run to finish.
```

This is the **live-contention** path. The already-open reports in this area — #10461 and #10779 — cover the opposite case, a lock left behind by an interrupted run whose owner PID is dead. Here the owner is alive and the operation is legitimately blocked; only the message is wrong.

Platform scope: Reproduced on macOS 26.5 (arm64), DGX Station GB300 (Ubuntu 24.04, aarch64), and a WSL2 aarch64 host; not platform-specific.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        Mac Studio (also reproduced on DGX Station GB300 and a WSL2 aarch64 host)
OS:            macOS 26.5
Architecture:  arm64
Node.js:       v22.23.1
npm:           10.x
Docker:        Docker version 29.5.2
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (the second command never reaches a sandbox)
```

## Steps to Reproduce

1. On a host with NemoClaw v0.0.119 installed, clear any resumable session:

   ```bash
   rm -f ~/.nemoclaw/onboard-session.json ~/.nemoclaw/onboard.lock
   ```

2. Start an ordinary onboarding in the background and let it get past preflight:

   ```bash
   nemoclaw onboard --name fence-a --agent openclaw --non-interactive --yes --fresh &
   sleep 25
   ```

3. While that run is still alive, start a second ordinary onboarding:

   ```bash
   nemoclaw onboard --name fence-b --agent openclaw --non-interactive --yes --fresh
   ```

4. Read the second command's output and exit code.

## Expected Result

The second command exits non-zero and tells the user what is happening: that another onboarding run holds the lock, which process holds it, and to wait for it to finish before retrying. That is the guidance the product already contains for this case.

## Actual Result

The second command exits 1 after about one second with a single internal line:

```text
Error: Cannot update onboarding recovery while another onboarding run owns the lock.
```

Checks run on the captured output:

```text
raw lock path shown to the user      : no
holder PID shown                     : no
"already in progress" guidance shown : no
wait-and-retry guidance shown        : no
```

The same shape appears for a rebuild started during an onboarding, and an uninstall started during an install reports the retry-exhaustion form instead:

```text
Error: Failed to acquire lock on <home>/.nemoclaw-portable-host.lock after 120 retries
```

That variant blocks for roughly two minutes before failing, with no indication that a competing operation is the reason.

## Logs

Not captured — the failure is the single error line quoted above plus the exit status.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `39581824493055c15d13fc1d27a8477395e2e602`.  There
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
{"case_id": "NVIDIA_NemoClaw__11052__3958182",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
