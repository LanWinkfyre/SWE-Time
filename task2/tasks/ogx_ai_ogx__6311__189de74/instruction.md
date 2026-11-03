# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Starter distribution enables trust_remote_code: true for sentence-transformers by default

### 🤔 What is the technical debt you think should be addressed?

 Commit `05f71b3f3` **(feat(responses): enable default memory vector store)** changed the sentence-transformers embedding provider configuration in the starter distribution from `trust_remote_code: false` to `trust_remote_code: true`. This affects:
  - src/ogx/distributions/starter/config.yaml
  - src/ogx/distributions/starter/run-with-postgres-store.yaml
  - src/ogx/distributions/starter/starter.py

  The config class itself documents this flag as defaulting to false for security reasons:
  ▎ "Whether to trust and execute remote code from model repositories. Set to True for models that require custom code (e.g., nomic-ai/nomic-embed-text-v1.5). Defaults to False for security."

With `trust_remote_code: true`, the sentence-transformers provider will execute arbitrary Python code bundled with any model loaded from the HuggingFace Hub. A compromised or malicious model repository could use this to achieve remote code execution on the OGX server.

Expected behavior: The starter distribution should default to trust_remote_code: false, matching the field's own default and the previous behavior.

Suggested fix: Revert the three files above to `trust_remote_code: false`. If a specific model needs it, document that in the model-specific setup instructions instead.

### 💡 What is the benefit of addressing this technical debt?

This change appears unrelated to the memory vector store feature that was the focus of the PR. If a specific embedding model requires `trust_remote_code`, the recommendation should be scoped to that model's documentation rather than enabled by default in the starter distribution, which is the template most new deployments start from.

### Other thoughts

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `189de747dca111f247d96404beb1e81e03c655a3`.  There
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
{"case_id": "ogx_ai_ogx__6311__189de74",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
