# Recover the symbolic verification state this change produces

A regression report was filed against `hashicorp/consul`.  The report is quoted verbatim below.

## Report

```
GUI elements disappear after upgrading to v1.22.x

#### Overview of the Issue

OS: Amazon Linux 2023 / Amazon Linux 2 / CentOS Stream 9
Browser: Firefox on the client side


After upgrading to **v1.22.1** from **v1.22.0**, GUI elements are missing from the left side navigation menu.

<img width="289" height="522" alt="Image" src="https://github.com/user-attachments/assets/36cd4e9f-e480-44b9-87b1-f2f56a9291e4" />

As you can see the menus for `Services`, `Nodes`, `Intentions`, etc. are missing.

What I expect to see is this:

<img width="288" height="670" alt="Image" src="https://github.com/user-attachments/assets/c39f68fa-4052-4cbd-9152-77909979db85" />



The paths are accessible, and if I directly type ...

`http://<consul-host-name>/ui/<region>/nodes`

... all the other elements show up in the GUI (As can be seen in the second screenshot)

#### Reproduction Steps

The GUI issue is reproducible even in `dev` mode. (`consul agent -dev`)

### Consul info for both Client and Server
version 1.22.1
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `554b4ba24f8680308afa7bbbdcc7494cedff7ea1`.  There
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
{"case_id": "hashicorp_consul__23082__554b4ba",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
