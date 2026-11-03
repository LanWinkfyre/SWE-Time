# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
No Docker support

Hi there you do not have Docker support.
I have created a Fallow Docker project in GitHub that works nicely, simplifying the installation greatly
This runs via a Docker Compose file in the Stacks folder /opt/stacks so it can be managed by Portainer
I am running this inside Windows 11 / Ubuntu Server

You are welcome to test and use my Docker Compose file 

https://github.com/nic0michael/fallow-in-docker

Kind regards
Nico
An Ex IBMer with 27 years of experience
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8d811649ba1750b819d43474a374fe81cb8a447e`.  There
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
{"case_id": "fallow_rs_fallow__1205__8d81164",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
