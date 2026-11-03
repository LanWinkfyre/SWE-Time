# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][CLI&UX] host probe ignores DOCKER_CONTEXT and calls a machine ready that onboard refuses

## Description

`nemoclaw host probe` ignores the selected Docker context. With `DOCKER_CONTEXT` pointing at a context whose endpoint is unreachable, and `DOCKER_HOST` unset, the probe resolves Docker through the default socket instead, reports the host as supported, and exits 0.

`nemoclaw onboard`, run seconds later on the same host with the same context selected, correctly refuses with a Docker authority conflict and exits 1.

The probe is the command a user runs to find out whether onboarding will work, so the two commands giving opposite answers about the same host at the same moment removes the value of the readiness check.

The probe does honor `DOCKER_HOST`. Pointed at the identical dead socket through `DOCKER_HOST` it correctly reports the host as incompatible and exits 2, which shows the gap is specific to the context selector rather than to unreachable endpoints in general.

Related: #11533 also reports `DOCKER_CONTEXT` being ignored, but on a different surface (the credential-helper path during managed sandbox image pull).

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
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. On a host where Docker is running and reachable through the default context, and a rootless Podman socket is also present, create a Docker context that points at a socket path where nothing is listening:

   ```bash
   docker context create qa-unreachable --docker host=unix:///run/user/$(id -u)/no-such.sock
   ```

2. Confirm the context really is dead, using the Docker CLI itself:

   ```bash
   DOCKER_CONTEXT=qa-unreachable docker version
   ```

3. With `DOCKER_HOST` unset, run the readiness probe against that selected context:

   ```bash
   unset DOCKER_HOST
   DOCKER_CONTEXT=qa-unreachable nemoclaw host probe
   echo "exit=$?"
   ```

4. Immediately afterwards, on the same host, run onboarding with the same selected context:

   ```bash
   DOCKER_CONTEXT=qa-unreachable nemoclaw onboard --name dock-conflict
   echo "exit=$?"
   ```

5. As a control, point the probe at the same dead socket through `DOCKER_HOST` instead of the context selector:

   ```bash
   DOCKER_HOST=unix:///run/user/$(id -u)/no-such.sock nemoclaw host probe
   echo "exit=$?"
   ```

6. Compare the three results.

## Expected Result

The probe honors the selected Docker context. When that context returns a definite unreachable result, the probe reports it rather than silently resolving Docker through a different endpoint, and its verdict agrees with what onboarding will do on the same host.

## Actual Result

Step 3, probe with the unreachable selected context:

```text
System readiness: supported
Findings:
- [warning] host.docker.storage_incompatible: The Docker storage configuration cannot
  support nested overlay mounts.
{"id": "host.docker.reachable", "state": "present", "value": true}
{"id": "host.docker.runtime", "state": "present", "value": "docker"}

exit=0
```

The host is called supported and Docker is called reachable. Nothing mentions the dead selected context, and no engine conflict is reported. Reproduced twice, roughly a minute apart.

Step 4, onboarding with the **same** selected context, seconds later:

```text
✗ Docker is not reachable. Please fix Docker and try again.
- Choose the Docker authority (docker_authority_conflict): The default Docker authority did
  not answer, and two engines answered on discovered sockets: docker at /run/docker.sock and
  podman at /run/user/{uid}/podman/podman.sock. ... it withholds the docker-group and
  start-Docker remedies while two other engines answer.
    export DOCKER_HOST='unix:///run/docker.sock'

exit=1
```

Onboarding correctly detects the problem and gives an accurate, actionable diagnosis. The probe did not.

Step 5, the control, same dead socket supplied through `DOCKER_HOST` rather than the context:

```text
System readiness: incompatible
Findings:
- [blocking] host.docker.daemon_unreachable

exit=2
```

So the probe handles an unreachable endpoint correctly when it arrives via `DOCKER_HOST`, and misses it entirely when it arrives via `DOCKER_CONTEXT`.

Net effect: a user who runs the readiness probe first is told the host is ready, then has onboarding refuse on the same host for a reason the probe never surfaced.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4c4de3abbda81fea3e85d2471a323d10f5f60739`.  There
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
{"case_id": "NVIDIA_NemoClaw__11719__4c4de3a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
