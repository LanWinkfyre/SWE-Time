# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Documentation contains more than 100 broken GitHub links

### System Info

Host OS: macOS on Apple Silicon
Test container: node:22-bookworm
Node.js: 22
npm: 10.9.8
OGX: 1.0.2
OGX commit: 9424b4d9e5eca99bfc79a6e0004e28adf5f58704
Component: documentation

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

```bash
curl -I https://github.com/ogx-ai/ogx-apps
curl -I https://github.com/ogx-ai/ogx-client-node
curl -I https://github.com/ogx-ai/ogx-client-kotlin
```

### Error logs

The links return HTTP 404.

```text
183 Markdown and MDX files scanned
576 distinct external URLs checked
109 GitHub URLs returned HTTP 404
```


### Expected behavior

### Expected result

Documentation should link to existing repositories and source files.
Remove or update the broken links and consider adding an external link checker to documentation CI.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4056d4bd6cdf5a6d9657d22914de871faa1e553b`.  There
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
{"case_id": "ogx_ai_ogx__6458__4056d4b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
