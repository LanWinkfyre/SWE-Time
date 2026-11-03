# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Allow disabling chat completions inference store

### 🚀 Describe the new functionality needed

Allow disabling Chat Completions persistence by setting the `inference` store reference to `null` in a run config:

```yaml
storage:
  stores:
    inference: null
```

Semantics when disabled:

- No `InferenceStore` is constructed, no `inference_store` table is created, and no background write workers are started — so no chat completion payload is ever persisted.
- The history endpoints (`list`, `retrieve`, `messages`) surface that persistence is not configured (HTTP 501).

### 💡 Why is this needed? What if we don't build it?

We host OGX internally as a shared service. By default the inference store persists every request/response payload, so the database fills up and there's currently no way to disable it. This caused a service outage the first time we ran into it. 

On top of that, we would like to guarantee zero data retention for our users. We currently run a nightly job on our Kubernetes cluster to delete data the inference store but this is not an ideal solution.

### Other thoughts

- Backward compatible by default: omitting the key keeps persistence enabled; only an explicit `inference: null` disables it. This follows the same optional-store pattern the Responses store already uses.
- Other stores (`responses`, `datasets`, `eval`, `files`, `prompts`, `vector_io`) are unaffected.
- Is `null` the right way to express "disable this store", or would a boolean (e.g. `inference.persist: false`) be preferable? Note the `responses` store is already `default=None`, so `null` matches existing config semantics.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5a5612b60c7c2794cd5aa4dc90764059da854e4b`.  There
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
{"case_id": "ogx_ai_ogx__6411__5a5612b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
