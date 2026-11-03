# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][CLI&UX] connect fails at the authority stage for any sandbox on a non-default gateway port, reporting a Hermes portable receipt on a plain OpenClaw sandbox

## Description

`nemoclaw {sandbox} connect` fails for any sandbox created on a non-default gateway port. The probe stops at the authority stage and reports a Hermes portable lifecycle receipt requalification, on a plain OpenClaw sandbox, on a host that has never used the portable profile. The same command against a sandbox on the default gateway succeeds.

Both sandboxes are healthy: each onboards with exit 0, reaches Ready, and `nemoclaw {sandbox} status` exits 0 either way. Only `connect` fails, and only on the non-default gateway.

The failure is not caused by credentials. The same command was run three times against one such sandbox - without an alternate provider credential, with one exported, and without one again - and produced the identical exit code and message every time.

Platform scope: Reproduced on two hosts, a DGX Spark aarch64 and an Ubuntu 24.04 x86_64; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        DGX Spark, and separately an Ubuntu 24.04 x86_64 host
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64 and x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.2.1, build a5c7197
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
One host, one variable - the gateway the sandbox is created on.

1. Confirm the host has never used the portable profile:
   ls -d "$HOME/.config/nemoclaw/portable" 2>/dev/null | wc -l      (expect 0)

2. Create a sandbox on a NON-DEFAULT gateway port:
   export NEMOCLAW_GATEWAY_PORT=18224
   export NEMOCLAW_OPENSHELL_GATEWAY_STATE_DIR="$HOME/gw224"
   mkdir -p "$HOME/gw224"; chmod 700 "$HOME/gw224"
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=ollama NEMOCLAW_MODEL=qwen2.5:1.5b \
     nemoclaw onboard --name conn-iso --non-interactive --no-gpu --fresh --yes \
     --yes-i-accept-third-party-software

3. nemoclaw conn-iso connect --probe-only
4. nemoclaw conn-iso status

5. Create a second sandbox on the DEFAULT gateway, with no port or state-dir override:
   unset NEMOCLAW_GATEWAY_PORT NEMOCLAW_OPENSHELL_GATEWAY_STATE_DIR
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=ollama NEMOCLAW_MODEL=qwen2.5:1.5b \
     nemoclaw onboard --name conn-def --non-interactive --no-gpu --fresh --yes \
     --yes-i-accept-third-party-software

6. nemoclaw conn-def connect --probe-only
```

## Expected Result

Step 3 behaves like step 6: the probe completes and reports that the OpenClaw gateway is running,
exit 0. A sandbox that onboarded successfully, reports Ready, and answers `status` cleanly should be
connectable regardless of which gateway port it was created on.

If a genuine authority problem exists, the message should describe it in terms of the sandbox and
gateway at hand, not a Hermes portable lifecycle receipt on a host where the portable profile has
never been used.

## Actual Result

```text
Both sandboxes onboard with exit 0 and reach Ready. Then:

  CASE 1 - isolated gateway (custom port + fresh state dir)
    onboard exit=0  phase: Ready
    ... result=failed failedStage=authority
    Error: Hermes portable lifecycle receipt schema-8 requalification requires the sandbox
           lifecycle lock for 'conn-iso'
    connect --probe-only exit=1
    status exit=0

  CASE 2 - DEFAULT gateway (no port or state-dir override)
    onboard exit=0  phase: Ready
    Probe complete: OpenClaw gateway is running in 'conn-def'.
    connect --probe-only exit=0
    status exit=0
```

## Logs

```text
Credential control on a third sandbox on a non-default gateway, same command three times:

  A - connect --probe-only with no alternate credential
      Error: Hermes portable lifecycle receipt schema-8 requalification requires the sandbox
             lifecycle lock for 'auth-bind-e'
      exit=1
  B - the same command with an alternate provider credential exported
      Error: Hermes portable lifecycle receipt schema-8 requalification requires the sandbox
             lifecycle lock for 'auth-bind-e'
      exit=1   (the credential value appears zero times in the output)
  C - back to no alternate credential
      Error: Hermes portable lifecycle receipt schema-8 requalification requires the sandbox
             lifecycle lock for 'auth-bind-e'
      exit=1

Host state at the time of the isolation run:
  portable directories on this host: 0
  agent: openclaw
  both sandboxes: phase Ready, status exit 0
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b08eaa0844dc2e972fbfa2806590668802d449b4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10783__b08eaa0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
