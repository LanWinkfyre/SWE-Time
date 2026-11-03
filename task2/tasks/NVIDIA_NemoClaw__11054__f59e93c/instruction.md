# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][CLI&UX] status on a DeepAgents Code sandbox intermittently exits 1 with no diagnostic

## Description

On a DeepAgents Code sandbox, `nemoclaw <sandbox> status` intermittently exits 1 while printing a complete, normal status report and emitting no error text on either stream. Roughly 30 percent of invocations fail this way. The same command against an OpenClaw sandbox on the same host, the same gateway and the same provider never fails.

Because the command prints a healthy Ready status and writes nothing to stderr beyond its usual gateway-selection line, neither a user nor automation can tell a real failure from this one. Any script that checks the exit code of a sandbox status call is unreliable on DeepAgents Code sandboxes.

- **Platform scope:** Reproduced on DGX Spark aarch64 only; other platforms not tested by this run.
- **Regression:** Unknown — earlier releases were not tested for this path.
- **OpenShell issue:** No. The failing command is NemoClaw's own status command.

## Environment

```text
Device:        NVIDIA DGX Spark
OS:            Ubuntu 24.04.3 LTS
Architecture:  aarch64
Kernel:        6.11.0-1014-nvidia
Node.js:       v22.22.1
npm:           10.9.4
Docker:        Docker version 28.3.3, build 980b856
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.119
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. On a DGX Spark host with NemoClaw v0.0.119 installed, onboard a DeepAgents Code sandbox. Onboarding exits 0.

   ```bash
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_YES=1 NEMOCLAW_PROVIDER=build \
     nemoclaw onboard --agent dcode --name <dcode sandbox> --yes
   ```

2. Onboard an OpenClaw sandbox on the same host as a control.

   ```bash
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_YES=1 NEMOCLAW_PROVIDER=build \
     nemoclaw onboard --agent openclaw --name <openclaw sandbox> --yes
   ```

3. Invoke status twenty times against each sandbox, recording the exit code each time.

   ```bash
   for i in $(seq 1 20); do nemoclaw <sandbox> status >/dev/null 2>&1; echo $?; sleep 2; done
   ```

4. Compare the two exit-code sequences.

## Expected Result

A read-only status command against a sandbox that is Ready either exits 0 every time, or, when it does exit non-zero, states why. The exit code and the reported state agree.

## Actual Result

The DeepAgents Code sandbox fails intermittently; the OpenClaw sandbox never does.

| Sandbox agent | Invocations | Exited 1 |
|---|---|---|
| DeepAgents Code | 20 | 6 |
| OpenClaw (control) | 20 | 0 |

Across three separate runs on the same host the DeepAgents Code totals were 5 of 10, 4 of 20 and 6 of 20 — 15 of 50 overall. The OpenClaw control was clean in 39 of 39 invocations across the same runs, including `status --json`.

On a failing invocation the command still prints the full report, ending with the usual runtime line, and stderr carries only the routine gateway-selection line. No diagnostic of any kind is emitted. The sandbox remains `Phase: Ready` throughout, and the very next invocation frequently exits 0 with byte-identical output.

## Logs

```text
Failing invocation, stderr in full:

  Active gateway set to 'nemoclaw'

Failing invocation, last lines of stdout:

      LangChain Deep Agents Code runtime: terminal

Exit code: 1
```

## Related issues — same family, not a duplicate

- #10709 — status exits non-zero because the managed inference route returns HTTP 503 while the sandbox reports Phase Ready. That report has a stated cause and a visible unhealthy inference line. This one has no 503, no unhealthy line and no diagnostic at all, and it is agent-specific rather than route-specific. Note #10709 was closed as not planned.
- #9280 — `connect --probe-only` exits 1 after restoring the dashboard forward. Different command, and a stated cause.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f59e93ce0abd06c6ecf4d2930c183dfe90c5e495`.  There
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
{"case_id": "NVIDIA_NemoClaw__11054__f59e93c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
