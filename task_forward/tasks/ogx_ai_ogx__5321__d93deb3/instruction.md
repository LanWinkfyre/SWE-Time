# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Implement more verbose inference metrics

### 🚀 Describe the new functionality needed

currently completions and chat/completions have a few metrics, but we need to add some of the following: 

```
llama_stack_tokens_per_second{...}

llama_stack_inference_duration_seconds{...}

llama_stack_time_to_first_token_seconds{...}
```

### 💡 Why is this needed? What if we don't build it?


1. **`llama_stack_inference_duration_seconds`** End-to-end latency from request arrival to completion. This is different from the generic `request_duration_seconds` because it measures only the inference time, excluding routing, auth, and middleware overhead. Critical for SLA monitoring and provider performance comparison.

2. **`llama_stack_time_to_first_token_seconds`** (streaming only) The time a user waits before seeing any output. This is the primary UX metric for streaming applications — a request might complete in 5s total but if the first token arrives in 200ms, the experience feels responsive. Without this, operators can't distinguish between "slow start + fast generation" vs "fast start + slow generation."

3. **`llama_stack_tokens_per_second`** Output throughput per request. This directly measures generation speed and is the standard metric for comparing inference backends. Combined with the `model` and `provider` attributes, it lets operators answer "which provider gives the best throughput for model X?" and detect throughput degradation.

All three metrics carry `model`, `provider`, `stream`, and `status` attributes, enabling per-model, per-provider, and streaming-vs-non-streaming breakdowns in dashboards like Grafana.

### Other thoughts

_No response_

Related: https://github.com/llamastack/llama-stack/issues/2596
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d93deb3be038b16e3524ff8ead80696f0fd93dfc`.  There
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
{"case_id": "ogx_ai_ogx__5321__d93deb3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
