# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][Docs] Gateway Lifecycle Authority page tells users to run systemctl against openshell-gateway.service, which does not exist

## Description

The published Gateway Lifecycle Authority page instructs the reader to inspect the gateway with

```bash
systemctl status openshell-gateway.service
systemctl --user status openshell-gateway.service
```

Neither unit exists. Both commands exit 4 with `Unit openshell-gateway.service could not be found.` The unit NemoClaw actually installs is named `nemoclaw-openshell-gateway.service`, and the string `nemoclaw-openshell-gateway` does not appear anywhere on the page.

A reader following the page to check gateway health gets a bare "could not be found" and has no way to tell whether the gateway is broken, was never installed, or the documentation is simply naming the wrong unit. It is the last of the three.

The page also shows a `"serviceName": "openshell-gateway.service"` value in a status example. On this build `nemoclaw status --json` reports a `gatewayAuthority` object with no `serviceName` field at all, so that example does not match the current output either.

Everything else on the page checked out on the same host and in the same session: `nemoclaw status` exits 0 and prints `Gateway authority: nemoclaw-managed`, `nemoclaw status --json` does expose a `gatewayAuthority` object, and `nemoclaw debug` does write `onboard-session-summary.txt` containing `gatewayAuthority` into its diagnostic bundle.

Page: `docs.nvidia.com/nemoclaw/user-guide/openclaw/deployment/gateway-lifecycle-authority`

Platform scope: The unit name is platform-independent; verified on Ubuntu 24.04 x86_64.
Regression: Unknown - earlier documentation revisions not compared.

## Environment

```text
Device:        Ubuntu 24.04 virtual machine
OS:            Ubuntu 24.04 LTS
Architecture:  x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.6.1
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.118
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
# 1. Open the published Gateway Lifecycle Authority page.

# 2. On a host with NemoClaw installed and a sandbox onboarded, run the two
#    commands the page gives, exactly as written:
systemctl status openshell-gateway.service ; echo $?
systemctl --user status openshell-gateway.service ; echo $?

# 3. List the units that actually exist:
systemctl --user list-unit-files | grep openshell
```

## Expected Result

The command printed on the page names the unit NemoClaw installs, so a reader can run it as written and see the gateway's state.

## Actual Result

```text
systemctl status openshell-gateway.service
  Unit openshell-gateway.service could not be found.
  exit 4

systemctl --user status openshell-gateway.service
  Unit openshell-gateway.service could not be found.
  exit 4

systemctl --user list-unit-files | grep openshell
  nemoclaw-openshell-gateway.service

nemoclaw status --json  ->  gatewayAuthority has these keys only:
  gatewayName, gatewayPort, mode, source, endpoint, supervisor,
  requiredCapabilities        (no serviceName)

The rest of the page verified correct on the same host:
  nemoclaw status              exit 0, prints "Gateway authority: nemoclaw-managed"
  nemoclaw status --json       contains a gatewayAuthority object
  nemoclaw debug ... -o FILE   bundle contains onboard-session-summary.txt,
                               and that file contains gatewayAuthority
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `19bb9860a662e25418f1afbc7e0589d7f22f2497`.  There
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
{"case_id": "NVIDIA_NemoClaw__10870__19bb986",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
