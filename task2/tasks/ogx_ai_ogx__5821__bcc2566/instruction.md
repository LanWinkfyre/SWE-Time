# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Broken links to external provider repos due to the rename

### System Info

N/A (documentation issue)

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

On the [Known External Providers](https://ogx-ai.github.io/docs/providers/external/external-providers-list) page, some of the repository names and links are wrong because they were changed during the project rename, but the repos are in other GitHub orgs and still use `llama-stack`. E.g. [`ogx-provider-kft`](https://github.com/opendatahub-io/ogx-provider-kft) should be [`llama-stack-provider-kft`](https://github.com/opendatahub-io/llama-stack-provider-kft) for KubeFlow Training provider

In addition, when trying to "Edit this page" directly from the docs site, it gave a 404. The `editUrl` field in `docusaurus.config.ts` is incorrect.

### Error logs

404 errors for repo links and edit page links

### Expected behavior

With the correct links (revert `ogx` back to `llama-stack` in the repo names) the repo page should load instead of throwing a 404.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bcc256609eafc55e48fc846d2b4b835171b0083c`.  There
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
{"case_id": "ogx_ai_ogx__5821__bcc2566",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
