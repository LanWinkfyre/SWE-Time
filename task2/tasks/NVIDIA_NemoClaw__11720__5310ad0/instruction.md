# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Install] gateway keeps holding port 8080 after systemctl stop reports success

## Description

The OpenShell gateway that the NemoClaw installer starts can outlive its own systemd user unit. The unit reports inactive and dead while the gateway process keeps running and keeps holding port 8080.

Stopping the unit does not stop the process. The stop command exits 0, reporting success, and the process is still listening afterwards. The only way to free the port is to kill the process directly, which the product never tells the user to do.

This is a dead end rather than an inconvenience. The port stays held, later onboarding attempts fail their gateway port preflight check, and the documented way to stop a gateway reports success while changing nothing, so the user has no reason to suspect the gateway is still running and no supported command that would stop it.

The state arises from an ordinary install. The installer starts this gateway on its own, so reaching it requires no unusual action by the user.

This blocked a release test case from reaching the behavior it was written to verify.

- **Platform scope:** Reproduced on Ubuntu 24.04 x86_64 only; other platforms not tested.
- **Regression:** Unknown — earlier versions not tested for this path.
- **OpenShell issue:** No

## Environment

```text
Device:        Ubuntu 24.04 host, x86_64, no GPU
OS:            Ubuntu 24.04.4 LTS
Architecture:  x86_64
Node.js:       Not on PATH (installer-managed Node.js)
npm:           Not on PATH (installer-managed Node.js)
Docker:        Docker version 29.8.0, build 88096ef
Podman:        podman version 5.7.0
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.123
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. Install NemoClaw v0.0.123 on a host with a running Docker daemon, using the ordinary installer. The installer starts an OpenShell gateway on its own.

2. Confirm the gateway is listening on port 8080:

   ```bash
   ss -lntp | grep 8080
   ```

3. Stop the Docker daemon:

   ```bash
   sudo systemctl stop docker
   ```

4. Check the state the gateway's own systemd user unit reports:

   ```bash
   systemctl --user is-active nemoclaw-openshell-gateway.service
   ```

5. Check whether the gateway process is actually still running and still holding the port:

   ```bash
   ss -lntp | grep 8080
   ```

6. Ask systemd to stop the unit, and record its exit code:

   ```bash
   systemctl --user stop nemoclaw-openshell-gateway.service
   echo "exit=$?"
   ```

7. Check the port again:

   ```bash
   ss -lntp | grep 8080
   ```

8. Attempt onboarding and observe the gateway port preflight result:

   ```bash
   NEMOCLAW_GATEWAY_RUNTIME=podman nemoclaw onboard --name podman-lane
   ```

## Expected Result

The gateway's lifecycle matches the unit that owns it. When the unit reports inactive, no gateway process is left running and the port is free.

Stopping the unit stops the gateway. If it cannot, the command reports the failure and names the process still holding the port, instead of exiting 0.

## Actual Result

Step 4, the unit reports the gateway is not running:

```text
inactive
```

Step 5, the process is nevertheless alive and holding the port on two addresses:

```text
LISTEN 0 128 {docker-bridge-ip}:8080 users:(("openshell-gatew",pid={pid},fd=15))
LISTEN 0 128  127.0.0.1:8080 users:(("openshell-gatew",pid={pid},fd=14))
```

Step 6, stopping the unit reports success:

```text
exit=0
```

Step 7, the port is still held by the same process after that successful stop:

```text
LISTEN 0 128 {docker-bridge-ip}:8080 users:(("openshell-gatew",pid={pid},fd=15))
LISTEN 0 128  127.0.0.1:8080 users:(("openshell-gatew",pid={pid},fd=14))
```

Killing the process directly by PID was the only way to free the port. After that, the port was confirmed free with no output from:

```bash
sudo lsof -i :8080 -sTCP:LISTEN -P -n
```

Step 8, while the port was still held, onboarding failed preflight:

```text
[1/8] Preflight checks
System readiness could not confirm required capabilities:
gateway.version.compatible, gateway.port.uncontested.
Gateway port 8080 could not be observed completely. Identify its listener before retrying:
sudo lsof -i :8080 -sTCP:LISTEN -P -n
```

The preflight message does point at the port, but the supported way to stop that gateway reports success without stopping it, so following the product's own guidance does not clear the condition.

Consequence for the affected test case: onboarding could not start, so the behavior under test was never reached.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5310ad0a5c25d49f06910525456ea2529506b3ae`.  There
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
{"case_id": "NVIDIA_NemoClaw__11720__5310ad0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
