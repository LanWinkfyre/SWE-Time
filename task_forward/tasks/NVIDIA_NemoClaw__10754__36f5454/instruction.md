# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Security] mcp status returns exit 0 for a managed MCP projection path replaced with a symlink or FIFO

## Description

`mcp status` does not detect or reject an unsafe file (dangling symlink, FIFO, or a symlink pointing at otherwise-valid content) placed at the managed MCP projection path. This was tested against three distinct unsafe-file scenarios and all three produced the identical result: exit code 0 and a generic "adapter mismatch" message, with no indication that the projection path itself is unsafe by type. The file-type safety check this path is expected to perform did not fire in any of the three cases tested (0 of 3).

Platform scope: Reproduced on Ubuntu 26.04 x86_64 with a Deep Agents Code sandbox; other agents/platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        x86_64 server, NVIDIA RTX PRO 6000 Blackwell Server Edition
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.7.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
OpenClaw:      N/A (Deep Agents Code sandbox tested; no OpenClaw sandbox involved in this repro)
```

## Steps to Reproduce

1. Onboard a Deep Agents Code sandbox and add a healthy managed MCP server (e.g. github):
   ```bash
   nemoclaw {sandbox} mcp add github --url https://api.githubcopilot.com/mcp/ --env GITHUB_MCP_TOKEN
   ```
   Confirm healthy: `nemoclaw {sandbox} mcp status github --json` (should show `credentialResolution.ok: true`).

2a. Scenario 1 — dangling symlink at the managed projection path:
   ```bash
   nemoclaw {sandbox} exec -- sh -lc 'rm -f /sandbox/.deepagents/.nemoclaw-mcp.json && ln -s /tmp/missing-nemoclaw-mcp.json /sandbox/.deepagents/.nemoclaw-mcp.json'
   nemoclaw {sandbox} mcp status github
   ```

2b. Scenario 2 — FIFO at the same path (restore a clean fixture first):
   ```bash
   nemoclaw {sandbox} exec -- sh -lc 'rm -f /sandbox/.deepagents/.nemoclaw-mcp.json && mkfifo /sandbox/.deepagents/.nemoclaw-mcp.json'
   nemoclaw {sandbox} mcp status github
   ```

2c. Scenario 3 — symlink to a copy of the original, otherwise-valid content (restore a clean fixture first):
   ```bash
   nemoclaw {sandbox} exec -- sh -lc 'cp /sandbox/.deepagents/.nemoclaw-mcp.json /tmp/valid-projection.json && rm -f /sandbox/.deepagents/.nemoclaw-mcp.json && ln -s /tmp/valid-projection.json /sandbox/.deepagents/.nemoclaw-mcp.json'
   nemoclaw {sandbox} mcp status github
   ```

## Expected Result

Each of the three `mcp status` calls in step 2a/2b/2c exits with a distinct, non-zero status that identifies the projection path as unsafe by type (symlink/FIFO), and does not report the provider as attached/healthy.

## Actual Result

All three scenarios produced functionally identical output and the identical exit code:

```text
MCP server: github
  agent: langchain-deepagents-code
  support: bridge
  endpoint: https://api.githubcopilot.com/mcp/
  provider attached: yes
  provider credentials: ready
  policy: present
  adapter: missing
  env: ready
  credential resolution: unknown (probe skipped: the managed agent
    adapter does not match the current credential revision)

EXITCODE:0
```

- Scenario 1 (dangling symlink): `EXITCODE:0`
- Scenario 2 (FIFO): `EXITCODE:0`
- Scenario 3 (symlink to valid content): `EXITCODE:0`

0 of 3 scenarios produced the expected non-zero, type-specific rejection. In every case the message is a generic "adapter mismatch / credential revision" message that does not mention the projection path, a symlink, a FIFO, or an unsafe file type at all — there is no observable difference in the tool's output between "the projection path was replaced with a malicious file" and "the credential happens to be mid-rotation."

## Logs

Not captured (terminal output above is the complete evidence for this defect).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `36f54548583a4db32b78b02a81df0222d7ef070b`.  There
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
{"case_id": "NVIDIA_NemoClaw__10754__36f5454",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
