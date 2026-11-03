# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Policy&Network] recover reports the dashboard forward restored and exits 0 while an unrelated process owns the port

## Description

When an unrelated local process already listens on a sandbox's dashboard forward port,
`nemoclaw {sandbox} recover` exits 0 and reports that the host forward was restored and that
launch readiness is healthy. The port is never taken over: the foreign process keeps the
listener for the whole operation, and an HTTP request to the dashboard URL is answered by the
foreign process, not by the sandbox.

The command is therefore telling the user that a forward it did not establish is ready. The
dashboard URL that NemoClaw prints carries an access token in its fragment, so a user who
follows the reported-healthy URL sends that token to whatever local process squatted the port.

Platform scope: Platform-specific not established; reproduced on DGX Spark aarch64 only, other
                platforms not tested for this path.
Regression: Unknown - earlier releases were not tested for this path.
OpenShell issue: No. The failing command is NemoClaw's own recover command.

## Environment

```text
Device:        NVIDIA DGX Spark
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Kernel:        6.17.0-1014-nvidia
Node.js:       v22.23.1
npm:           10.9.8
Docker:        Docker version 29.2.1, build a5c7197
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.120
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. Onboard an OpenClaw sandbox with a dashboard enabled and record its forward port:
     nemoclaw {sandbox} dashboard-url --quiet

2. Stop the sandbox so it releases the forward:
     nemoclaw {sandbox} stop

3. Start an unrelated listener on the freed port and confirm it is serving:
     python3 -m http.server {port} --bind 127.0.0.1 &
     ss -ltnp | grep :{port}
     curl -fsS "http://127.0.0.1:{port}/" -o /tmp/pre.html

4. Ask NemoClaw to recover the sandbox and record the exit code:
     nemoclaw {sandbox} recover; echo "RECOVER_EXIT=$?"

5. Re-check who owns the port and what answers on it:
     ss -ltnp | grep :{port}
     curl -fsS "http://127.0.0.1:{port}/" -o /tmp/post.html
```

## Expected Result

Recovery exits non-zero, names the occupied or unverified-owner port, and withholds launch
readiness. The foreign listener is left running and untouched.

## Actual Result

The foreign listener is correctly left untouched, but recovery reports success:

  RECOVER_EXIT=0
  Probe complete: OpenClaw gateway is running in {sandbox}.
  ... forwardAction=restored result=ready

Port ownership before and after recovery is identical and belongs to the foreign process:

  LISTEN 0 5 127.0.0.1:{port} 0.0.0.0:* users:(("python3",pid={foreign pid},fd=3))

The dashboard request before and after recovery both return the same 9433-byte directory
listing produced by the foreign process, so nothing of the sandbox is reachable on the port
that recovery just declared restored.

Reproduced twice on the same host in independent runs.

## Logs

```text
Foreign listener log, showing it served both requests and was never signalled:

  127.0.0.1 - - [07/Sep/2026 06:35:58] "GET / HTTP/1.1" 200 -

Process state after recovery:

  PID STAT CMD
  {foreign pid} S python3 -m http.server {port} --bind 127.0.0.1
```

## Related Bugs / not duplicate of

Same area, different symptom, not a duplicate:

- **#7085** — recover reported a port-forward failure when the forward was already active. That is the inverse symptom of this report and is already fixed. Worth checking whether that fix removed the occupied-port rejection path this report needs.
- **#7227** — stop left NemoClaw's own dashboard forward alive and status flagged a port conflict. That concerns a forward NemoClaw itself owns; this report concerns a listener owned by an unrelated process.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4eaa7c1c222acd38868cdfe8703884b3e99ab10e`.  There
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
{"case_id": "NVIDIA_NemoClaw__11149__4eaa7c1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
