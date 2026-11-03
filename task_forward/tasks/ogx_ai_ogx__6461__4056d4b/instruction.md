# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Unit test script fails in a clean dev env

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
git checkout v1.0.2
./scripts/unit-tests.sh --tb=short -q
```

### Error logs

```text
ModuleNotFoundError: No module named qdrant_client
```

### Expected behavior

The script installs the unit dependency group but qdrant-client is not included in that group.

The same test suite passes only after the additional CI setup step:
```bash
uv sync --all-groups
```
After this undocumented setup, the result is:

```text
2468 passed
3 skipped
3 xfailed
```

### Expected result

The documented unit test command should work in a clean development environment.
Please include all required test dependencies in the unit group or document and enforce the required setup step.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4056d4bd6cdf5a6d9657d22914de871faa1e553b`.  There
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
{"case_id": "ogx_ai_ogx__6461__4056d4b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
