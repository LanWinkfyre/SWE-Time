# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][CLI&UX] policy add and policy remove print "Preset not found" for the custom preset they just applied or removed

## Description

When a custom preset is applied or removed with `nemoclaw {sandbox} policy add --from-file` / `policy remove`, the command succeeds and the live OpenShell policy is updated correctly, but the output also prints `Preset not found: {name}` for the very preset it just applied or removed. On remove the contradictory line is printed twice, interleaved with the correct progress lines.

The operation itself is correct — the policy version is submitted and loaded, the egress is opened and later narrowed, and the preset shows up as user-added in `policy list` while it is applied. Only the reporting is wrong, and it is wrong in a way that reads as a failure on a command that exited 0.

Platform scope: Reproduced on WSL2 Ubuntu 24.04 x86_64 only; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        WSL2 guest on a Windows host
OS:            Ubuntu 24.04.4 LTS on WSL2 (microsoft-standard-WSL2 kernel, 6.18 series)
Architecture:  x86_64
Node.js:       v22.23.0
npm:           10.9.8
Docker:        Docker version 29.5.3, build d1c06ef
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```text
1. Onboard any sandbox, for example:
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=ollama NEMOCLAW_MODEL=qwen2.5:1.5b \
     nemoclaw onboard --fresh --non-interactive --no-gpu --name rt424 --yes \
     --yes-i-accept-third-party-software

2. Write a valid custom preset:

   preset:
     name: qa-doc-check
     description: "doc validation fixture"
   network_policies:
     qa_doc_check:
       name: qa_doc_check
       endpoints:
         - host: "api.example.com"
           port: 443
           protocol: rest
           enforcement: enforce
           rules:
             - allow: { method: GET, path: "/**" }
       binaries:
         - { path: /usr/bin/curl }

3. Apply it:   nemoclaw rt424 policy add --from-file /tmp/ok.yaml
4. Confirm it is present:  nemoclaw rt424 policy list
5. Remove it:  nemoclaw rt424 policy remove qa-doc-check --yes
```

## Expected Result

Step 3 prints the applied-preset confirmation and nothing that contradicts it.
Step 5 prints the removed-preset confirmation and nothing that contradicts it.
Neither command reports the preset as not found while it is acting on that exact preset.

## Actual Result

```text
Step 3 — apply succeeds but ends with a contradictory pair of lines:

  Policy version 3 submitted (hash: 94002d5bd477)
  Policy version 3 loaded (active version: 3)
  Applied preset: qa-doc-check
  Preset not found: qa-doc-check
  [exit=0]

Step 5 — remove succeeds, and the contradictory line appears twice, before and between the correct
progress lines:

  Preset not found: qa-doc-check
  Endpoints that would be removed: api.example.com
  Preset not found: qa-doc-check
  Narrowing sandbox egress — removing: api.example.com
  Policy version 4 submitted (hash: fb62d82b293f)
  Policy version 4 loaded (active version: 4)
  Removed preset: qa-doc-check
  [exit=0]
```

## Logs

```text
Between steps 3 and 5, policy list confirms the preset really is applied, so the "not found" line is
inconsistent with the command's own view of state:

  Policy presets for sandbox 'rt424':
    ...
    - qa-doc-check [user-added] - custom OpenShell policy

  qa-doc-check present in policy list: 1

Reproduced identically on two separate runs against two different sandboxes on the same build, one on
gateway port 18298 and one on 18299.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c0f23b6058034432133f9fcc0b9e024ba03c95b6`.  There
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
{"case_id": "NVIDIA_NemoClaw__10775__c0f23b6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
