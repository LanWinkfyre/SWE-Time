# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
If you add opus as a backend via api, then add a model via the api that should use llama.cpp or vllm, it then tries to use opus

**LocalAI version:**
v4.1.3 (fdc9f7bf350b05942323f5f4b264480c7b67b51c)

**Environment, CPU architecture, OS, and Version:**
Docker, X64, Ubuntu 24.04

**Describe the bug**
(I'm scripting an install to deploy to multiple people.)
If you curl to add opus which is required for realtime and then opus loads and then you then script any llm model you want that would normally use llama.cpp it will then try and use opus instead of being specified as llama.cpp and thus inducing a download of the required backend

**To Reproduce**
```
        payload="{\"id\":\"opus\"}"
	response="$(curl -fsS -X POST "${LOCALAI_BASE_URL}/backends/apply" \
		"${AUTH_HEADER[@]}" \
		-H "Content-Type: application/json" \
		-d "${payload}")"

        payload="{\"id\":\"Qwen3.5-9b\"}"
	response="$(curl -fsS -X POST "${LOCALAI_BASE_URL}/models/apply" \
		"${AUTH_HEADER[@]}" \
		-H "Content-Type: application/json" \
		-d "${payload}")"


```
**Expected behavior**
this should induce the model to use the proper backend that is in the default configuration.

One would also expect that if the model allowed multiple backends (i.e. llama.cpp and vllm-omni) that you'd be able to choose the backend as part of the payload to the request.

**Logs**
N/A.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `185956154a8bfd7d8e640da1aec879b6b2193bf6`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__9287__1859561",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
