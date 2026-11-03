# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][Sandbox] destroy --cleanup-gateway leaves the shared gateway running and prints no gateway message on the last sandbox

## Description

On Linux, `nemoclaw {sandbox} destroy --cleanup-gateway --yes` against the last remaining sandbox exits 0 but leaves the shared OpenShell gateway service running and the gateway port bound. The destroy output contains no gateway-related messaging at all in this case — not a cleanup confirmation, and not the usual "Shared NemoClaw gateway preserved... pass `--cleanup-gateway`... next time" hint that normally prints when the flag is omitted.

Platform scope: Reproduced on Ubuntu 24.04 only; other platforms not tested.
Regression: Unknown — earlier versions not tested.

## Environment

```text
Device:        Ubuntu 24.04 x86_64 server, NVIDIA GPU
OS:            Ubuntu 24.04
Architecture:  x86_64
Node.js:       v22.22.3
npm:           10.9.8
Docker:        29.5.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.122
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. Onboard a fresh sandbox so exactly one sandbox is registered:
   ```bash
   nemoclaw onboard --agent openclaw --name {sandbox} --non-interactive --fresh --yes
   ```
2. Confirm the gateway port is bound:
   ```bash
   ss -tlnp | grep 8080
   ```
3. Run:
   ```bash
   nemoclaw {sandbox} destroy --cleanup-gateway --yes
   ```
4. Confirm this really was the last sandbox, both via the registry and the live OpenShell state:
   ```bash
   nemoclaw list
   openshell sandbox list -g nemoclaw -o json
   ```
5. Re-check the gateway port and service state:
   ```bash
   ss -tlnp | grep 8080
   systemctl --user status nemoclaw-openshell-gateway.service
   ```

## Expected Result

Since this is confirmed as the last sandbox and `--cleanup-gateway` was passed explicitly, the shared gateway service should stop and the gateway port should be released. This is the behavior implied by NemoClaw's own destroy output on other runs (see Logs) — the hint text explicitly says passing `--cleanup-gateway` achieves cleanup.

## Actual Result

Destroy exits 0 with no gateway-related output at all. Step 4 confirms zero live/registered sandboxes (both `nemoclaw list` and `openshell sandbox list -g nemoclaw -o json` report empty). Despite that, step 5 shows the gateway service still active (running) and the gateway port still bound by the openshell-gateway process — the shared gateway was not cleaned up even though `--cleanup-gateway --yes` was passed on the confirmed last sandbox.

## Logs

Destroy output (no gateway-cleanup or gateway-preserved messaging present):
```text
  Deleting sandbox '{sandbox}'...
  Removed managed agent state volume for '{sandbox}'.
[services] cloudflared was not running
  Sandbox '{sandbox}' destroyed
```

For comparison, a destroy WITHOUT `--cleanup-gateway` on the last sandbox normally prints:
```text
  Shared NemoClaw gateway preserved. Re-run 'openshell gateway remove nemoclaw' to remove it,
  or pass '--cleanup-gateway' / set NEMOCLAW_CLEANUP_GATEWAY=1 next time.
```

`systemctl --user status nemoclaw-openshell-gateway.service` after the `--cleanup-gateway` destroy:
```text
Active: active (running)
```

`ss -tlnp | grep 8080` after the `--cleanup-gateway` destroy:
```text
LISTEN 0 128 127.0.0.1:8080 0.0.0.0:* users:(("openshell-gatew",...))
LISTEN 0 128 {docker-bridge-ip}:8080 0.0.0.0:* users:(("openshell-gatew",...))
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `052c19e9a7f65d0ea3dd2e6e6202aa27fe7ef476`.  There
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
{"case_id": "NVIDIA_NemoClaw__11540__052c19e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
