# Recover the symbolic verification state this change produces

A regression report was filed against `hashicorp/consul`.  The report is quoted verbatim below.

## Report

```
Navigating to the Consul UI services page shows error in the UI, Consul v1.22.4

### Overview of the Issue

When navigating to the Consul UI services page (/ui/dc1/services), the UI displays error.
```
Consul returned an error
You may have visited a URL that is loading an unknown resource, so you can try going back to the root or try re-submitting your ACL Token/SecretID by going back to ACLs.
```

### Reproduction Steps

1. Upgrade to Consul v1.22.4
2. Visit the UI at /ui/dc1/services
3. Shows "Consul returned an error" displayed on the page

### Consul Version

1.22.4

### Browser and Operating system details

- Browser: Chrome (latest)
- OS: Windows 11
- Node type: Single-node server (bootstrap_expect = 1)
- Connect: Enabled with Nomad-registered sidecar proxies

### Screengrabs / Web Inspector logs

GET /v1/catalog/datacenters →  200 OK
GET /v1/internal/ui/services →  200 OK

Note:
The error persists in the UI despite the API being healthy.
ACL is disabled.
Downgrade to the Consul v1.21.2, (other versions between 1.21.2 and 1.22.4 not checked)


<img width="1049" height="886" alt="Image" src="https://github.com/user-attachments/assets/6abaf1bd-a60c-4e11-bfd8-797c1b1c5180" />
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
{"case_id": "hashicorp_consul__23238__554b4ba",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
