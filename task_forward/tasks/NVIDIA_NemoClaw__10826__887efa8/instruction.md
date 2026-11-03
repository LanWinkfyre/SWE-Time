# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Hermes LKG install rejects the release base image after tracked-pin qualification fails

## Priority

High. The default LKG Hermes install can fail after any tracked base-image pull or runtime-qualification failure.

## Description

The served installer defaults to `lkg`, which currently resolves to NemoClaw v0.0.109. Hermes base-image resolution tries the Dockerfile-tracked digest first. If that candidate does not resolve or pass the runtime qualification, the resolver continues to version, source-commit, nearest-version, and `latest` candidates.

A fallback candidate can pass compatibility checks but still lack the tracked-pin provenance required by the final Hermes image guard. On v0.0.109, the source and release image resolves to `ghcr.io/nvidia/nemoclaw/hermes-sandbox-base@sha256:c613a1051f29a8e907345062e3162aabd0c693a277a6cc0893b7aed811ea9ce1`. The guard then stops onboarding with:

```text
Error: Hermes final image does not accept base image ref 'ghcr.io/nvidia/nemoclaw/hermes-sandbox-base@sha256:c613a1051f29a8e907345062e3162aabd0c693a277a6cc0893b7aed811ea9ce1'; use the tracked official digest or a repository-built local base
```

The guard prevents NemoClaw from using an unaccepted base image. The bug is the resolver path that selects a candidate the guard must reject and replaces the original tracked-pin failure with a misleading final error.

## Local reproduction

The failure was reproduced from commit `d027b770d7130685d020964c4811211baf3d5f31`, which is both v0.0.109 and the current `lkg` target.

Environment:

- macOS host with a Linux/arm64 Docker daemon
- Docker 29.2.1
- Node.js 22.23.2
- No v0.0.109 Hermes base image present before the cold run

Results:

1. A normal cold resolver run completed in 38.9 seconds and selected the tracked `ffafa4dd...` digest.
2. A second run injected only one failed MCP runtime qualification for the tracked digest. NemoClaw source and all other Docker operations remained unchanged.
3. The unmodified resolver selected `c613a105...` and threw the same exception at `dist/lib/agent/base-image.js:455`.
4. The `c613a105...` image then passed the real MCP runtime probe in 0.72 seconds.

This proves that the defect is conditional, but any tracked-pin pull or qualification failure can reach it. The fallback image is functional; its provenance is not accepted by the final Hermes image guard.

## Expected behavior

When Hermes requires the Dockerfile-tracked base image and that candidate fails resolution or qualification, NemoClaw must not continue to a candidate that the final Hermes guard cannot accept.

NemoClaw must retain the fail-closed trust boundary and report the tracked candidate's failure. A bounded retry is permitted only for the same immutable tracked digest and read-only qualification operation.

## Acceptance criteria

- [ ] A failed tracked Hermes candidate does not fall through to version, source-commit, nearest-version, or `latest` candidates that lack tracked-pin provenance.
- [ ] The command reports the tracked candidate's pull or qualification failure instead of a later final-image guard error.
- [ ] A valid tracked index digest and its Docker-normalized platform digest remain accepted with pinned provenance.
- [ ] Explicit trusted operation leases and repository-built local bases retain their current behavior.
- [ ] Other agents retain their current base-image candidate order.
- [ ] Regression coverage exercises the exact sequence: tracked Hermes candidate fails, a source or version candidate could pass, and resolution stops before that fallback.
- [ ] Negative coverage proves that an unaccepted fallback digest is never passed to Hermes sandbox-image creation.

## Security boundary

The final Hermes image guard is authoritative for accepted base-image provenance. The fix must not broaden accepted repositories, digests, sources, overrides, or trust leases.

## Related work

- #7058 — previous intermittent release-image fallback failure
- #10598 — v0.0.115 tracked-image capability mismatch during rebuild
- #6308 and #6313 — earlier platform-digest normalization failures
- #10824 — separate default gateway-port conflict found during the same user install
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `887efa89b75e558275dca3be5c372d92c60575da`.  There
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
{"case_id": "NVIDIA_NemoClaw__10826__887efa8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
