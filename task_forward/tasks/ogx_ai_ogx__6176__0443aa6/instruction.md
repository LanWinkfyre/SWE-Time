# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Improve the documented API schema

### 🤔 What is the technical debt you think should be addressed?

Currently the documented API spec is very vague especially in its "leaf nodes". 

The good example can be the `tools.OpenAIResponseInputToolFileSearch.ranking_options.ranker` field (https://ogx-ai.github.io/docs/api/create-openai-response-v-1-responses-post). It does not define any possible values but what's provided there affects the chosen reranker. **How should I know what to provide**? 

There are many other similar vaguely documented fields.

### 💡 What is the benefit of addressing this technical debt?

Clear, structured API schema leaving nothing to second guessing or trying manually. 
Professional documentation making it really easy to try out the OGX almost out-of-the-box. 

### Other thoughts

It should also be noted, very explicitly, that the OGX server's configuration hugely affects the sent requests and has multitude of default values kicking-in when the request specifies not-expected values (but the **expected values are undocumented** 🙃).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0443aa634a1fa0f1e7fb2070874988653e245e39`.  There
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
{"case_id": "ogx_ai_ogx__6176__0443aa6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
