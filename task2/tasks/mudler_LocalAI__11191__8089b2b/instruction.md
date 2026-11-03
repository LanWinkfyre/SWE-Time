# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Generic option passthrough doesn't work

LocalAI version:
localai/localai:master-gpu-hipblas
sha256:8f6d98239653cd94a76d845ccffae1688f14f2d793c6a1341e5f1e2ef41d43d3

Environment, CPU architecture, OS, and Version:
I'm doing this on unraid 7.3, using portainer.
AMD Ryzen 9 5900X
Radeon AI PRO R9700
Local AI is setup using distribution mode with nodes.

**Describe the bug**
When trying to use any [generic option passthrough](https://localai.io/advanced/model-configuration/index.html#generic-option-passthrough) it fails to start.

And it's failing with this error
```
Jul 29 12:41:09 INFO  Upload skipped (file already exists with matching hash) node="9456dd90-14d3-4f97-bdf6-1ec79bb9f4ac" key="models/laguna-s-2.1-118b-a8b/llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf" remotePath="/models/laguna-s-2.1-118b-a8b/llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf" 

Jul 29 12:41:09 INFO  Loading model on remote node node="rocinante-worker" model="llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf" addr="la-rocinante-worker:50053" payloadBytes=33766781984 loadBudget=15m11.775457493s 

Jul 29 12:41:09 ERROR Failed to load model modelID="laguna-s-2.1-118b-a8b" error=failed to route model with internal loader: routing model llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf: loading model laguna-s-2.1-118b-a8b: loading model llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf on node rocinante-worker: rpc error: code = Unavailable desc = error reading from server: EOF backend="llama-cpp-development" 

Jul 29 12:41:09 ERROR Stream ended with error error=failed to route model with internal loader: routing model llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf: loading model laguna-s-2.1-118b-a8b: loading model llama-cpp/models/laguna-s-2.1-118b-a8b/Laguna-S-2.1-UD-IQ1_S.gguf on node rocinante-worker: rpc error: code = Unavailable desc = error reading from server: EOF 
```

It's dying on the frontend before it even hits the node

**To Reproduce**
Download this model and try to run it using yaml it'll error
```
backend: llama-cpp
cache_type_k: q8_0
cache_type_v: q8_0
context_size: 524288
flash_attention: true
function:
    automatic_tool_parsing_fallback: true
    grammar:
        disable: true
known_usecases:
    - chat
name: laguna-xs-2.1-33b-a3b
options:
    - use_jinja:true
    - parallel:2
    - cache_type_k:q8_0
    - cache_type_v:q8_0
    - "--override-tensor:exps=CPU"
parameters:
    model: llama-cpp/models/laguna-xs-2.1-33b-a3b/Laguna-XS-2.1-Q4_K_M.gguf
    repeat_penalty: 1
    temperature: 0.6
    top_k: 20
    top_p: 0.95
repeat_penalty: 1
temperature: 0.6
template:
    use_tokenizer_template: true
top_k: 20
top_p: 0.95
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8089b2bf0998428975da076d06faab592fd415e6`.  There
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
{"case_id": "mudler_LocalAI__11191__8089b2b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
