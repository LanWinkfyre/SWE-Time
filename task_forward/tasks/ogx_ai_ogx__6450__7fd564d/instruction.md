# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Official installer references a docker image that does not exist

### System Info

Host OS: macOS on Apple Silicon
Docker: Docker Desktop 28.5.1
Docker image: docker.io/ogx/distribution-starter:latest
OGX: 1.0.2

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The official installer defaults to docker.io/ogx/distribution-starter:latest, but this dockerhub repository is not publicly available.

```bash
docker pull docker.io/ogx/distribution-starter:latest
```

### Error logs

Docker cannot pull the image and the dockerhub API returns HTTP 404 with object not found.

### Expected behavior

The following tags were also unavailable:

```text
ogx/distribution-starter:latest
ogx/distribution-starter:1.0.2
ogx/distribution-starter:v1.0.2
```

### Expected result

The image used by the official installer should be publicly available and versioned.
Please publish the expected image or update the installer to use the correct registry and image name.

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
{"case_id": "ogx_ai_ogx__6450__7fd564d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
