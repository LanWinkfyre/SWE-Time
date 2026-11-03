# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[BSD] Process.gids() returns saved user ID instead of saved group ID

On FreeBSD, OpenBSD and NetBSD the `saved` field of `Process.gids()` returns the process saved *user* ID (`ki_svuid` / `p_svuid`) instead of the saved group ID (`ki_svgid` / `p_svgid`). Copy-paste bug introduced in 2011 (83466ce9). It went unnoticed because uid and gid usually coincide numerically (root, per-user groups).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `86fed5b7105a6177c67a022a5020d190f41a10e1`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "giampaolo_psutil__2905__86fed5b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
