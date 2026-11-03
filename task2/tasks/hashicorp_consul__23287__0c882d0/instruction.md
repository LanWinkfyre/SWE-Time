# Recover the symbolic verification state this change produces

A regression report was filed against `hashicorp/consul`.  The report is quoted verbatim below.

## Report

```
Broken UI with 1.22.5?

<!--- When filing a bug, please include the following headings if possible. Any example text in this template can be deleted. --->

### Overview of the Issue
with 1.22.5, UI for me is broken. Using same configuration, 1.22.0 is good. Specifically, nodes and services are not showing up, k/v shows up fine. ACL is enabled, APIs work fine, just the UI is broken

<img width="1314" height="443" alt="Image" src="https://github.com/user-attachments/assets/c6604934-9be6-40a0-8c7f-d751bd2a079f" />

### Reproduction Steps

--->

<!--- Steps to reproduce this issue/view the area for improvement, eg:  --->
1. Upgrade from 1.22.0 to 1.22.5 - same consul.hcl configuration
2. Visit the UI page at `/ui/services`
3. View error/area.

### Describe the solution you'd like

Nodes and services should be listed

### Consul Version

<!--- This can be found either in the footer of the UI (Consul versions pre 1.10) or
at the top of the help menu that is in the top right side of the UI. --->
1.22.5
### Browser and Operating system details
RHEL8 Linux

<!--- Browser, Browser Version, OS, and any other information you can provide about the environment that may be relevant. --->

### Screengrabs / Web Inspector logs

<!--- If you think it's worthwhile, include appropriate screengrabs showing the
error/area for improvement. Try to include the URL bar of the browser so we
can see the current URL where the error manifests. Please be careful to
obfuscate any sensitive information either in the URL or in the browser page
itself. --->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0c882d0bdc8f82529569bce9ad8e1ec5d636240d`.  There
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
{"case_id": "hashicorp_consul__23287__0c882d0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
