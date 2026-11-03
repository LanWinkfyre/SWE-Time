# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
UI production dependencies include critical and high severity vulnerabilities

### System Info

Host OS: macOS on Apple Silicon
Test container: node:22-bookworm
Node.js: 22
npm: 10.9.8
OGX: 1.0.2
OGX commit: 9424b4d9e5eca99bfc79a6e0004e28adf5f58704
Component: src/ogx_ui

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

```bash
cd src/ogx_ui
npm ci
npm audit --omit=dev
```

### Error logs

```text
1 critical vulnerability
3 high severity vulnerabilities
```

### Expected behavior

### Expected result

Production dependencies should not include known critical or high severity vulnerabilities, please tackle with affected packages or document why the reported vulnerabilities are not exploitable in the OGX deployment model.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f73a00f47083741128030653fcbf64ea71949dfe`.  There
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
{"case_id": "ogx_ai_ogx__6452__f73a00f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
