# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Release automation: keep the Dockerfile FALLOW_VERSION and checksums in lockstep with releases

The Dockerfile pins `ARG FALLOW_VERSION` plus two per-arch sha256 digests for the `fallow-linux-x64-musl` and `fallow-linux-arm64-musl` release assets, verified with `sha256sum -c` during the image build. Those three values only move when someone edits them by hand, so the default image drifts one release at a time: it sat on 2.94.0 until #1805 bumped it to 3.3.0.

Proposal: make the release pipeline own the bump. After the binaries are published, a release step computes the two digests from the just-uploaded assets and rewrites the ARG plus both sha256 lines (as part of the release commit flow, or as an automated follow-up right after the assets exist). The lockstep rule is already documented in the Dockerfile comment; this turns it from a convention into a mechanism.

Acceptance: after a release completes, `docker build` with no `--build-arg` produces the just-released version, and the checksum verification passes for both arches without any manual edit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `acc994aa8ec24673399d016db7dede091338c8e7`.  There
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
{"case_id": "fallow_rs_fallow__1817__acc994a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
