# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
OGX UI docs reference unavailable image ogx/ui

### System Info

N/A

### Information

- [x] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The [OGX UI docs page](https://ogx-ai.github.io/docs/distributions/ogx_ui#option-2-using-docker) (`docs/docs/distributions/ogx_ui.mdx` in this repository) provides instructions to run OGX UI in a container.

```sh
docker run -p 8322:8322 ogx/ui
```

The referenced image `ogx/ui` is not available to me on Docker Hub. The organization [ogx](https://hub.docker.com/u/ogx) is similarly not available.

The organization [ogxai](https://hub.docker.com/u/ogxai) does not contain a UI related image, only the starter and postgres-demo distributions.

### Error logs

Output of `podman run -p 8322:8322 docker.io/ogx/ui`:

```
Trying to pull docker.io/ogx/ui:latest...
Error: unable to copy from source docker://ogx/ui:latest: initializing source docker://ogx/ui:latest: reading manifest latest in docker.io/ogx/ui: requested access to the resource is denied
```

### Expected behavior

I expect commands in the documentation to run as documented (assuming prerequisites are met). In this case I would expect `docker run -p 8322:8322 ogx/ui` to download the `ogx/ui` image and run a container with the OGX UI.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `016a6079594de71b58cba2e58842126fadda2ec1`.  There
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
{"case_id": "ogx_ai_ogx__6370__016a607",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
