# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
refactor(cli): share operation-local Podman executable proof

## Outcome
Create one adapter-owned opaque Podman executable proof per Hermes operation and share it across all bound engines without changing validation frequency.

## Parent
Subissue of #10822.

## Scope and security
Preserve canonical PATH resolution, full constructor validation, per-command checks, immutable authority IDs, socket authority, managed-bootstrap/workload-cleanup behavior, and rejection of caller-forged proofs.

## Acceptance
- Proof is constructible only by the Podman adapter.
- Host doctor, local inference, lifecycle, and mutation engines share one operation-local proof.
- No process-global/path cache.
- Legacy validation sequencing and managed root helpers remain covered.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b08eaa0844dc2e972fbfa2806590668802d449b4`.  There
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
{"case_id": "NVIDIA_NemoClaw__10922__b08eaa0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
