# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Failed to replace output token: {es}


### Discussed in https://github.com/emmercm/igir/discussions/1615

<div type='discussions-op-text'>

<sup>Originally posted by **HDZEE** June 15, 2025</sup>
I’m trying to go through a large batch of ReDump games but I get random “failed to replace output token: {es}” and the whole process is aborted. I can rerun the command with an added —input-dir-exclude but with 62,000+ files I just have keep running the command and add exclusions as they come up. 

Is there a way to have igir skip the files it has errors for instead of stopping the whole process? 

Please help, thanks</div>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7df48dd2ae1ddc6768ab70bd57a2227f5c34762b`.  There
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
{"case_id": "emmercm_igir__1617__7df48dd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
