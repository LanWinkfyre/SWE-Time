# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
v1.0.2 CLI fails with MCP 2.x after a clean installation

### System Info

Host OS: macOS on Apple Silicon
Docker: Docker Desktop 28.5.1
Test container: ghcr.io/astral-sh/uv:python3.12-bookworm
Container platform: linux/amd64
Python: 3.12
uv: 0.9.30
OGX: 1.0.2
OGX commit: 9424b4d9e5eca99bfc79a6e0004e28adf5f58704

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

```bash
docker run --rm --platform linux/amd64 \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  bash -lc "uvx --from ogx==1.0.2 ogx --help"
```

### Error logs

ImportError: cannot import name McpError from mcp

### Expected behavior

A clean installation resolves mcp==2.1.1. OGX v1.0.2 declares mcp>=1.23.0 and imports McpError, while MCP 2.x exports MCPError.

### Expected result
ogx --help should work after installing the published package.

The current main branch constrains MCP to <2.0, but the submitted v1.0.2 release remains affected. Please publish a corrected release and update the version referenced by the JOSS submission.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7fd564d79c6b4709943ec2e50ad0c69c95f7718e`.  There
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
{"case_id": "ogx_ai_ogx__6449__7fd564d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
