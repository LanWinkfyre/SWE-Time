# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Integration test runner omits required provider dependency setup

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
uv sync --all-groups
./scripts/integration-tests.sh \
  --stack-config ci-tests \
  --suite base \
  --setup ollama \
  --inference-mode replay
```

### Error logs

```text
100 failed
94 passed
248 skipped
1 deselected
1 xfailed
```

The repeated root cause is:
```text
No module named sentence_transformers
```

### Expected behavior

### Expected result

The integration test runner should either install the required provider dependencies or fail early with a clear setup command.
Please make the local integration test workflow reproduce the CI environment without requiring knowledge of hidden CI action steps.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `952262240ff44ca3ba169efe87dc8a2deea76bfd`.  There
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
{"case_id": "ogx_ai_ogx__6462__9522622",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
