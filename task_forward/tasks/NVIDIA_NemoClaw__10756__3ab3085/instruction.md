# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Sandbox] snapshot restore fails deterministically when an unsafe file sits at the MCP projection path

## Description

`snapshot restore` fails deterministically (3 out of 3 attempts) when an unsafe file (dangling symlink or FIFO) has been placed at the managed MCP projection path inside the sandbox. The restore reports a failed file and leaves the sandbox not fully returned to the clean snapshot state — the unsafe file itself is also left in place afterward.

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

1. Onboard a Deep Agents Code sandbox, add a healthy managed MCP server, and create a snapshot while it is healthy:
   ```bash
   nemoclaw {sandbox} snapshot create --name qa-clean
   ```
2. Replace the managed MCP projection file with an unsafe type, e.g. a dangling symlink:
   ```bash
   nemoclaw {sandbox} exec -- sh -lc 'rm -f /sandbox/.deepagents/.nemoclaw-mcp.json && ln -s /tmp/missing-nemoclaw-mcp.json /sandbox/.deepagents/.nemoclaw-mcp.json'
   ```
3. Attempt to restore the snapshot:
   ```bash
   nemoclaw {sandbox} snapshot restore qa-clean --yes
   ```
4. Repeat step 2 (using a FIFO instead of a symlink this time) and step 3 again.

## Expected Result

The restore completes successfully, exits 0, and returns the sandbox (including the projection path) to the clean snapshot state.

## Actual Result

Both attempts (symlink case and FIFO case) failed identically:

```text
Using snapshot v1 name=qa-clean
Restoring snapshot into '{sandbox}'...
Restore failed.
Partial: .state, skills
Failed files: config.toml
EXITCODE:1
```

The unsafe file at the projection path remained in place after each failed restore attempt — the sandbox was not returned to Ready/clean state either time.

## Logs

Not captured (terminal output above is the complete evidence for this defect).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3ab308534bf5fdc4346ee14a6603f6377408827f`.  There
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
{"case_id": "NVIDIA_NemoClaw__10756__3ab3085",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
