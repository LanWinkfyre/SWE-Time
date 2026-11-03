# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Missing gateway declaration selector can start competing gateway and select wrong registry

### Investigation Summary

- A host had a valid external gateway declaration at `/etc/nemoclaw/gateway-management.json` and an active systemd-supervised gateway at `https://127.0.0.1:18080`.
- With `NEMOCLAW_GATEWAY_MANAGEMENT` set, onboarding and post-reboot status attached to `nemoclaw-18080`; the original sandbox was `Ready` and healthy.
- With the declaration selector absent from one non-login process, `nemoclaw <name> status` silently started a second, NemoClaw-managed gateway on port 8080.
- The command then selected the port-8080 registry and falsely reported that the live port-18080 sandbox did not exist.
- This was discovered while retesting #7404, but it is independent of that DGX Spark post-reboot report.

### Description

When a platform provides an externally supervised OpenShell gateway and a gateway-management declaration, one NemoClaw process that does not inherit `NEMOCLAW_GATEWAY_MANAGEMENT` can silently fall back to historical self-managed behavior.

In the reproduced case, the fallback started a competing gateway named `nemoclaw` on port 8080 even though the platform gateway `nemoclaw-18080` was active. Because NemoClaw registries are segregated by gateway port, the status command then read the empty port-8080 registry and reported that the sandbox did not exist.

Expected behavior: NemoClaw must not silently establish a second gateway authority when a trusted host declaration or conflicting platform authority is discoverable. It should either resolve the trusted declaration consistently or stop with a clear error before starting another gateway. The fix must retain the current self-managed fallback on hosts that genuinely have no external declaration.

### Reproduction Steps

1. Provision a Linux host with:
   - an externally supervised OpenShell gateway on port 18080;
   - a valid declaration at `/etc/nemoclaw/gateway-management.json`;
   - `NEMOCLAW_GATEWAY_MANAGEMENT=/etc/nemoclaw/gateway-management.json` available to the intended login environment.
2. In that environment, onboard `example` and confirm that it is registered with `nemoclaw-18080`.
3. Confirm `nemoclaw example status` exits 0 and reports the sandbox `Ready`.
4. Start a new process without `NEMOCLAW_GATEWAY_MANAGEMENT`, `NEMOCLAW_GATEWAY_PORT`, or `NEMOCLAW_OPENSHELL_GATEWAY_ENDPOINT`.
5. Run `nemoclaw example status`.
6. Observe that NemoClaw starts a new gateway on port 8080 and reports `Sandbox 'example' does not exist.`
7. List gateway registrations and observe both `nemoclaw` at port 8080 and `nemoclaw-18080` at port 18080.

### Environment

- OS: Ubuntu 22.04, x86_64
- Host: NemoClaw Daily Tag Brev Launchable (`env-3IfCEIUngquJuSZbOQrPMGd3FXm`)
- NemoClaw: v0.0.119
- OpenShell: v0.0.106, Docker driver
- Gateway mode: externally supervised by `openshell-gateway.service`
- Intended gateway: `nemoclaw-18080`, `https://127.0.0.1:18080`
- Inference: OpenAI-compatible NVIDIA endpoint; no credential values are included here

### Debug Output

Targeted, redacted evidence was collected before running any repair operation:

```text
$ env | grep -E '^NEMOCLAW_(GATEWAY_MANAGEMENT|GATEWAY_PORT|OPENSHELL_GATEWAY_ENDPOINT)='
(no output)

$ nemoclaw example status
[2/8] Starting OpenShell gateway
Starting OpenShell Docker-driver gateway...
Docker-driver gateway is healthy
Sandbox 'example' does not exist.
Run 'nemoclaw onboard' to create one.
exit=1

$ openshell gateway list
NAME             ENDPOINT
nemoclaw         https://127.0.0.1:8080
nemoclaw-18080   https://127.0.0.1:18080
```

Running the same status command in an environment containing the declaration selector selected `nemoclaw-18080`, reported the sandbox `Ready` and Docker health `healthy`, and exited 0.

The unintended port-8080 process was verified by executable path, command line, PID file, and listening port before it was stopped. Its gateway registration was then removed. The intended port-18080 gateway and sandbox remained healthy.

### Logs

```shell
Direct process without the declaration selector:
  Starting OpenShell gateway...
  Gateway log: /home/ubuntu/.local/state/nemoclaw/openshell-docker-gateway/openshell-gateway.log
  Docker-driver gateway is healthy
  Sandbox 'example' does not exist.

Process identity created by that command:
  executable=/usr/local/bin/openshell-gateway
  command=openshell-gateway[nemoclaw=nemoclaw;port=8080]
  listener=127.0.0.1:8080
```

### Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d8fb8822833b6c60d3a1d984b9d0c6b5d7f6d56f`.  There
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
{"case_id": "NVIDIA_NemoClaw__11347__d8fb882",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
