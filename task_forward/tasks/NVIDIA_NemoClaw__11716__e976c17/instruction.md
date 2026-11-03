# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Onboard] Podman onboarding rejects Podman's own default socket folder permissions

## Description

On the native rootless Podman path (`NEMOCLAW_GATEWAY_RUNTIME=podman`), onboarding stops at preflight and reports that the Podman socket authority is writable by another user or group. The rejected state is the one Podman itself creates by default: Podman's own systemd socket unit ships `SocketMode=0660` and creates its runtime directory at mode `0755`.

Because Podman produces this layout on its own, a freshly prepared host always fails. The only hosts that pass are ones where the socket directory mode was already changed by an earlier successful run.

No other user can actually reach the socket. The directory's own parent is mode `0700`, and the socket's group is the user's private group with no other members, so the group bit grants no real access to any other principal.

The printed remedy does not apply. It asks the user to start a rootless Podman 5 API service, but the service is already running and answering; following the instruction changes nothing. The message never names the directory, its mode, or the change that would clear the check, so there is no user-discoverable way out.

This blocked two release test cases from reaching the behavior they were written to verify.

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

1. On a host with rootless Podman 5.7.0 installed, enable and start the user-scoped Podman socket so it is created by Podman itself, with no manual permission changes:

   ```bash
   systemctl --user enable --now podman.socket
   ```

2. Confirm the layout Podman created. The socket directory is mode `0755` and the socket is mode `0660`, both owned by the current user:

   ```bash
   stat -c "%n %a %U:%G" /run/user/$(id -u)/podman
   stat -c "%n %a %U:%G" /run/user/$(id -u)/podman/podman.sock
   ```

3. Confirm the mode is Podman's shipped default rather than local configuration:

   ```bash
   systemctl --user cat podman.socket | grep SocketMode
   ```

4. Confirm no other user can reach the socket. The parent runtime directory is mode `0700` and the socket's group is the user's own private group with an empty member list:

   ```bash
   stat -c "%n %a" /run/user/$(id -u)
   getent group $(id -gn)
   ```

5. Confirm the Podman API is live and answering:

   ```bash
   podman info --format "{{.Host.RemoteSocket.Exists}}"
   ```

6. Start onboarding on the native rootless Podman path:

   ```bash
   NEMOCLAW_GATEWAY_RUNTIME=podman nemoclaw onboard --name podman-lane
   ```

## Expected Result

Preflight accepts the socket layout that Podman creates by default and onboarding continues.

If a stricter permission model is genuinely required, the check names the exact directory and mode it rejects and states the change that would satisfy it, and that requirement is documented on the Podman deployment page.

## Actual Result

Onboarding exits 1 during preflight step `[1/8]` with:

```text
✗ Podman runtime: Podman socket authority is writable by another user or group.
  start a rootless Podman 5 API service on Linux and retry
```

The suggested remedy has no effect, because the rootless Podman API service is already running and answering at the time of the failure (confirmed in step 5 above).

**A two-arm control isolates the socket directory mode as the single cause.** Both arms ran the same command on the same host, minutes apart, with nothing else changed.

Arm 1 — directory left at Podman's default mode `0755`:

```text
$ stat -c "sockdir %a" /run/user/$(id -u)/podman
sockdir 755
$ NEMOCLAW_GATEWAY_RUNTIME=podman nemoclaw onboard ...
  [1/8] Preflight checks
  ✗ Podman runtime: Podman socket authority is writable by another user or group.
```

Arm 2 — directory changed to mode `0700`, nothing else touched:

```text
$ chmod 700 /run/user/$(id -u)/podman
$ stat -c "sockdir %a" /run/user/$(id -u)/podman
sockdir 700
$ NEMOCLAW_GATEWAY_RUNTIME=podman nemoclaw onboard ...
  [1/8] Preflight checks
  (the socket-authority rejection does not appear; preflight proceeds)
```

A separate check confirms Podman recreates the rejected mode on its own. Removing the runtime directory and restarting the socket unit produced mode `0755` again with no user involvement:

```text
$ systemctl --user stop podman.socket
$ rm -rf /run/user/$(id -u)/podman
$ systemctl --user start podman.socket
$ stat -c "sockdir: %a %U:%G" /run/user/$(id -u)/podman
sockdir: 755 {user}:{user}
$ stat -c "socket : %a %U:%G" /run/user/$(id -u)/podman/podman.sock
socket : 660 {user}:{user}
```

The same host reports `SocketMode=0660` from Podman's shipped socket unit, so both the socket mode and the directory mode are Podman defaults, not local customization.

For contrast, a second host that had previously completed a NemoClaw run already had the directory at mode `0700` and did not hit this rejection, which is consistent with the directory mode being the deciding factor.

No documentation on the Podman deployment or troubleshooting pages mentions this error text or asks the user to change the socket directory permissions.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e976c17505e3038cfb1411439feafba123a1a159`.  There
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
{"case_id": "NVIDIA_NemoClaw__11716__e976c17",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
