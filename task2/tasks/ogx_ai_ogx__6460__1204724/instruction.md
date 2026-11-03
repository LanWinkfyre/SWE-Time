# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
v1.0.2 uv.lock is inconsistent with pyproject.toml

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
uv lock
git diff --exit-code uv.lock
```

### Error logs

uv.lock is modified

pyproject.toml requires:

```text
ogx-client==1.0.2
```

uv.lock contains:

```text
ogx-client==1.0.1
```

Running uv lock updates six lockfile references from 1.0.1 to 1.0.2.


### Expected behavior

### Expected result

Running uv lock on the release tag should not change uv.lock.
Regenerate the lockfile and include the corrected version in the submitted release.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `120472441707537e92f70c5caec38b65a444d0c5`.  There
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
{"case_id": "ogx_ai_ogx__6460__1204724",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
