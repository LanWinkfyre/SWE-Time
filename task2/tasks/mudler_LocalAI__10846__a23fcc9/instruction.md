# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
backend not found: cloud-proxy

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

Hello,

I tried to use my own llama.cpp OpenAI compatible backend in localai but it seems the `cloud-proxy` backend is nowhere to be found ?

**LocalAI version:**
`localai/localai:latest-gpu-hipblas`

**Environment, CPU architecture, OS, and Version:**
`uname -a` : `Linux fwd 7.1.3-2-cachyos #1 SMP PREEMPT_DYNAMIC Wed, 08 Jul 2026 06:14:22 +0000 x86_64 GNU/Linux`
OS: CachyOS
Server: Framework Desktop `AMD RYZEN AI MAX+ 395 w/ Radeon 8060S` with 128GB ram

**Describe the bug**
When trying to use a OpenAI Cloud Proxy provider it fails with `Error: code=500, message=cloudproxy: load cloud-proxy backend: failed to load model with internal loader: backend not found: cloud-proxy`

**To Reproduce**
`+ Add Model` > `OpenAI Cloud Proxy` > Fill out > `Create Model` > go chat with the model > error

**Expected behavior**
cloud-proxy backend should be present and relay to the backend server

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->

Model YAML:
```yaml
backend: cloud-proxy
known_usecases:
    - chat
name: gemma4-test
pii:
    enabled: true
proxy:
    api_key_env: OPENAI_API_KEY
    mode: passthrough
    provider: openai
    request_timeout_seconds: 120
    upstream_model: gemma4
    upstream_url: https://<omitted>/v1/chat/completions
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a23fcc90c36b49439a1a3bd785f8854c1816021e`.  There
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
{"case_id": "mudler_LocalAI__10846__a23fcc9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
