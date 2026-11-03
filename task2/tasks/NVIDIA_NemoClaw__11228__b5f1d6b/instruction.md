# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Publish release tags for the Hermes managed image (ghcr.io/nvidia/nemoclaw/hermes-sandbox) like openclaw-sandbox

### Problem Statement

NemoClaw publishes the complete managed image for OpenClaw (`ghcr.io/nvidia/nemoclaw/openclaw-sandbox:<release>`), so a downstream project can build a custom sandbox the way the docs describe ([Install OpenClaw Plugins](https://docs.nvidia.com/nemoclaw/latest/user-guide/openclaw/manage-sandboxes/install-openclaw-plugins)) without vendoring the NemoClaw checkout: `FROM` the published image, add a plugin, `nemoclaw onboard --from Dockerfile`.

For Hermes only the intermediate image is published (`ghcr.io/nvidia/nemoclaw/hermes-sandbox-base`). The complete image the `managed-images` workflow builds from `agents/hermes/Dockerfile` (`ghcr.io/nvidia/nemoclaw/hermes-sandbox`) has no tag on GHCR (checked `v0.0.114`, `v0.0.113`, `v0.0.110`, `latest`). The docs say not to use a `sandbox-base` alone as a final image, and `agents/hermes/Dockerfile` copies from a dozen repository-root paths, so a downstream Hermes image today has to reproduce that Dockerfile with a version-matched NemoClaw checkout as build context.

Concrete case: NVIDIA VSS (`NVIDIA-AI-Blueprints/video-search-and-summarization`, PR #2024) ships an OpenClaw sandbox image under `agent-harness/openclaw/` that extends `openclaw-sandbox` with the VSS skills and a plugin; its Hermes sandbox still has to be provisioned at run time (`nemoclaw <sandbox> skill install`, `upload`) because there is no `hermes-sandbox` image to extend.

### Desired Behavior

`ghcr.io/nvidia/nemoclaw/hermes-sandbox:<release>` (and a digest) is published for every release alongside `openclaw-sandbox`, from the same `managed-images` lane that already defines it, with the same platform coverage.

Before: a downstream Hermes Dockerfile must start from `hermes-sandbox-base` (unsupported as a final image) or from a NemoClaw checkout.
After: `FROM ghcr.io/nvidia/nemoclaw/hermes-sandbox@sha256:… AS nemoclaw-runtime`, add skills/plugins, `nemoclaw onboard --agent hermes --from Dockerfile`, exactly like the OpenClaw path.

### Scope and Exclusions

Includes: publishing the already-built complete Hermes image and documenting the custom-image workflow for Hermes (the Hermes counterpart of *Install OpenClaw Plugins*). Excludes: any change to `agents/hermes/Dockerfile` itself, to the Hermes runtime, or to the plugin/skill install commands. If `hermes-sandbox` is intentionally unpublished (e.g. size, licensing of a bundled component), the ask reduces to documenting that and the supported downstream path.

### Ongoing Ownership

NemoClaw managed-images owners (the lane already builds this artifact). Downstream consumer: the VSS blueprint team (NVIDIA-AI-Blueprints/video-search-and-summarization), who will maintain `agent-harness/hermes/` on top of it.

### Placement and Support Expectations

Core NemoClaw: this is the existing managed-image publication extended to one more agent that the workflow already builds. Support expectation is the same as for `openclaw-sandbox`: per-release tag plus digest, release notes noting the pinned Hermes version.

### Validation Plan

- `docker manifest inspect ghcr.io/nvidia/nemoclaw/hermes-sandbox:<release>` resolves for the release that ships the change, for the same platforms as `openclaw-sandbox`.
- `nemoclaw onboard --non-interactive --agent hermes --name <sb> --from <Dockerfile>` with a Dockerfile that is only `FROM ghcr.io/nvidia/nemoclaw/hermes-sandbox@<digest>` plus `USER sandbox` reaches a healthy sandbox (`nemohermes <sb> status`, dashboard reachable).
- The existing Hermes e2e lane (`managed-image-activation-e2e`) passes against the published tag rather than a locally rebuilt image.

### Compatibility Requirements

Same matrix as `openclaw-sandbox`: linux/amd64 (and arm64 where the Hermes lane builds it), NemoClaw releases from the one that ships this change onward, OpenShell Docker and Kubernetes drivers.

### Security or Privacy Impact

None new: the image is already built and validated by the release workflow; this only publishes it. Downstream images that extend it inherit the managed startup, config hash verification and gateway health check instead of re-implementing them from `sandbox-base`, which is a reduction in downstream drift.

### Implementation Idea

`managed-images.yaml` already declares `repository: ghcr.io/nvidia/nemoclaw/hermes-sandbox` for the Hermes lane. Enable the push (and digest publication step used for `openclaw-sandbox`) for that lane on release tags.

### Category

Feature

### Checklist

- [x] I searched existing issues and this is not a duplicate
- [x] I described the problem and desired behavior
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b5f1d6bbb0e01c78015094c1d650a051bbaf82a6`.  There
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
{"case_id": "NVIDIA_NemoClaw__11228__b5f1d6b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
