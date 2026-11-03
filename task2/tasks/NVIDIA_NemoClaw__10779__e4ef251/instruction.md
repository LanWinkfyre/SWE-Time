# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][CLI&UX] an interrupted onboard leaves a per-gateway onboard.lock that blocks nemoclaw list and uninstall with no stale-lock diagnosis or remedy

## Description

Interrupting `nemoclaw onboard` leaves an `onboard.lock` file under the gateway's state directory. The lock survives the interrupted process, and afterwards unrelated NemoClaw commands on that gateway port refuse to run - including the read-only `nemoclaw list` and `nemoclaw uninstall`. The refusal message talks about migrating legacy state and does not say that a stale lock is present, that its owner is gone, or how to clear it, so there is no path forward from the message itself.

Removing the lock file restores normal operation immediately, which is what identifies it as the cause.

This is a different file and a different failure than the known interrupted-onboard lock problem on the portable host lock, which affects `onboard --resume` and retries 120 times before giving up. Here the lock is per-gateway-port, no retry happens, and the commands blocked are ordinary read and uninstall commands rather than a resume.

Platform scope: Reproduced on two separate DGX Spark aarch64 hosts running the same build; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        DGX Spark (two separate hosts, same result)
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.2.1, build a5c7197
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. Start an onboarding run against a chosen gateway port and let it reach the sandbox-creation step:

   NEMOCLAW_GATEWAY_PORT=18273 NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=ollama \
     NEMOCLAW_MODEL=qwen2.5:1.5b nemoclaw onboard --fresh --non-interactive --no-gpu \
     --name fxi --yes --yes-i-accept-third-party-software

2. Interrupt it with SIGINT once it prints "Creating sandbox".

3. Confirm the lock is present:
   ls -l "$HOME/.nemoclaw/gateways/18273/onboard.lock"

4. Run an ordinary command against that port:
   NEMOCLAW_GATEWAY_PORT=18273 nemoclaw uninstall --yes

5. On a second host, do the same and then run the read-only listing instead:
   NEMOCLAW_GATEWAY_PORT=18310 nemoclaw list

6. Remove the lock and repeat step 5:
   rm -f "$HOME/.nemoclaw/gateways/18310/onboard.lock"
   NEMOCLAW_GATEWAY_PORT=18310 nemoclaw list
```

## Expected Result

Either the interrupted run does not leave a lock behind, or a lock whose owning run is no longer alive is
recognised as stale and reclaimed. Read-only commands such as `nemoclaw list` should not be blocked by an
onboarding lock at all. If a command genuinely must refuse, the message should say that a stale onboarding
lock is present, identify it, and state how to clear it.

## Actual Result

```text
Step 4 - uninstall refuses, exit 1:

  Cannot safely migrate legacy NemoClaw state for this gateway port: onboarding lock
  /home/{user}/.nemoclaw/gateways/18273/onboard.lock is present; finish or stop that run
  before migrating state
  [exit=1]

Step 5 - the read-only listing refuses with the same message, exit 1:

  Cannot safely migrate legacy NemoClaw state for this gateway port: onboarding lock
  /home/{user}/.nemoclaw/gateways/18310/onboard.lock is present; finish or stop that run
  before migrating state
  [exit=1]

Step 6 - after removing the lock file, the same command succeeds, exit 0:

  Incomplete onboarding:
    nochannel  interrupted at sandbox
  [exit=0]

There is no run left to "finish or stop" - the onboarding process has already exited.
```

## Logs

```text
Two-way control on one host, same command either side of the lock removal:

  lock kind: regular file
  ### list WITH the stale lock present
  exit=1
    Cannot safely migrate legacy NemoClaw state for this gateway port: onboarding lock
    /home/{user}/.nemoclaw/gateways/18310/onboard.lock is present; finish or stop that run
    before migrating state
  lock removed
  ### list WITHOUT the lock
  exit=0

Independent reproduction on the second host, blocking uninstall after a SIGINT during onboarding:

  starting a real onboarding on port 18273 and interrupting it before any sandbox is registered
    gateway dir appeared: YES
    reached the sandbox-creation step: 1
  $ NEMOCLAW_GATEWAY_PORT=18273 nemoclaw uninstall --yes
    Cannot safely migrate legacy NemoClaw state for this gateway port: onboarding lock
    /home/{user}/.nemoclaw/gateways/18273/onboard.lock is present; finish or stop that run
    before migrating state
  [exit=1]
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e4ef251490902737909b7d2710c41ed549a07243`.  There
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
{"case_id": "NVIDIA_NemoClaw__10779__e4ef251",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
