# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Station][Security] CHAT_UI_URL silently binds the Hermes dashboard on all interfaces; remote hosts reach it with a spoofed loopback Host

## Description

Setting CHAT_UI_URL to an external HTTPS address - the documented way to put the Hermes dashboard behind a reverse proxy - silently changes the dashboard port forward from a loopback bind to a bind on all interfaces. The user is never asked for this and is never told it happened.

The exposure is real, not theoretical. From a different machine on the network the port accepts TCP connections and serves the dashboard HTML, and the Host check in front of it is not an access control: sending the trivially guessable header {Host: 127.0.0.1:PORT} returns HTTP 200 and the full dashboard page.

Two things make this hard for a user to notice. First, non-loopback binding is supposed to be an explicit opt-in through NEMOCLAW_DASHBOARD_BIND, and that variable was unset throughout. Second, the CLI keeps reporting the dashboard as loopback: both {nemoclaw list} and {sandbox dashboard-url} print an address on 127.0.0.1 for the very sandbox whose forward is bound on all interfaces, so the displayed address contradicts the actual listener.

Isolated with a single-variable control on one host: the same sandbox name, the same command, the same port, and NEMOCLAW_DASHBOARD_BIND unset in both runs. The only difference is whether CHAT_UI_URL is set.

Platform scope: Reproduced on DGX Station GB300 (aarch64, Ubuntu 24.04); other platforms not tested.
Regression: Unknown - earlier versions not tested for this path.
OpenShell issue: No

## Environment

```text
Device:        DGX Station GB300
OS:            Ubuntu 24.04 LTS
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.2.1
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.118
OpenClaw:      2026.7.1
Agent:         NemoHermes
```

## Steps to Reproduce

```bash
NEMOCLAW_DASHBOARD_BIND must be unset for every step.

1. Onboard a Hermes sandbox WITHOUT CHAT_UI_URL, then record the bind address of
   its dashboard port:

     nemohermes onboard --name bind-ctl --non-interactive --fresh --yes --no-gpu
     nemoclaw list                 note the dashboard port it prints
     ss -ltn | grep PORT

2. Destroy it and onboard the same name again, changing only CHAT_UI_URL:

     nemoclaw bind-ctl destroy --yes
     CHAT_UI_URL=https://dashboard.example.com/ nemohermes onboard --name bind-ctl \
       --non-interactive --fresh --yes --no-gpu
     nemoclaw list                 note the dashboard port
     ss -ltn | grep PORT

3. Compare what the CLI reports with the actual listener:

     nemoclaw list
     nemohermes bind-ctl dashboard-url

4. From a DIFFERENT machine on the same network, request the port directly:

     curl -s -o /dev/null -w '%{http_code}' http://TEST-HOST:PORT/
     curl -s -w '%{http_code}' -H 'Host: 127.0.0.1:PORT' http://TEST-HOST:PORT/
```

## Expected Result

Configuring an external browser-facing URL does not change the bind address. The dashboard forward stays on 127.0.0.1 unless the operator explicitly opts in with NEMOCLAW_DASHBOARD_BIND=0.0.0.0, which is the documented control for widening the listening surface.

A request from another machine is refused at the TCP layer, exactly as it is for a sandbox onboarded without CHAT_UI_URL.

If the product does decide to widen the bind, it says so during onboarding and the address it reports afterwards matches the address it is actually listening on.

## Actual Result

```text
Single-variable control, same host, same sandbox name, same port 18793:

  without CHAT_UI_URL    LISTEN 127.0.0.1:18793
  with CHAT_UI_URL       LISTEN 0.0.0.0:18793

NEMOCLAW_DASHBOARD_BIND was unset in both runs.

The same split is visible across four sandboxes on the host at once. Only the one onboarded with CHAT_UI_URL is bound on all interfaces:

  LISTEN 0.0.0.0:18792     hermes-proxy-valid   (CHAT_UI_URL set)
  LISTEN 127.0.0.1:18790   hermes-loopback-a    (not set)
  LISTEN 127.0.0.1:18791   hermes-loopback-b    (not set)

What the CLI reports for all of them, including the exposed one:

  nemoclaw list                        dashboard: http://127.0.0.1:18792/
  nemohermes {sandbox} dashboard-url   Dashboard URL: http://127.0.0.1:18792/

From a different machine on the network, against the exposed port:

  no Host override               HTTP 400  Invalid Host header.
  Host: 127.0.0.1:18792          HTTP 200  721 bytes, Hermes Agent - Dashboard
  Host: dashboard.example.com    HTTP 200  721 bytes, Hermes Agent - Dashboard

Control from the same remote machine against a loopback-bound port:

  http://TEST-HOST:18790/        curl exit 7, connection refused

So the Host check does not restrict access: a remote caller who guesses the
loopback Host value reaches the dashboard.
```

## Logs

```text
Remote response body, first bytes, fetched from another machine with a spoofed
loopback Host header:

  <!doctype html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Hermes Agent - Dashboard</title>

Listener ownership on the host, showing the forward process holding the port:

  LISTEN 0 128 0.0.0.0:18792 0.0.0.0:* users:(("ssh",pid=PID,fd=3))
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7e4bdf27f17bd760a02e36467d7ea79a9ae5a37e`.  There
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
{"case_id": "NVIDIA_NemoClaw__10861__7e4bdf2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
