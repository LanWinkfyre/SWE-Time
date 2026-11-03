# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Hitting /api/tags gives models with :latest tag, but you cannot specify tagged models like that with the other endpoints (even ollama ones)

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
<!-- Container Image or LocalAI tag/commit -->
LocalAI v4.9.0 (f7ad3f70eb5d8a0ddf80e08557f0d7df28cf032e)

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->
lenovo pgx (which is essentially a dgx spark) running dgx os 
```Darwin mypgx 25.4.0 Darwin Kernel Version 25.4.0: Thu Mar 19 19:30:44 PDT 2026; root:xnu-12377.101.15~1/RELEASE_ARM64_T6000 arm64```

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->

if you send a request to /api/tags, it returns a list of models tagged with :latest. But if you try to specify a model when calling (f.e.) /api/chat, you need to omit the tag. This breaks discovery with many apps (in my case, im trying to use oh my pi) 

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->
```bash
 curl http://localhost:8080/api/tags | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3449    0  3449    0     0  79589      0 --:--:-- --:--:-- --:--:-- 80209
{
  "models": [
    {
      "name": "qwen3.8-27b-q4:latest",
      "model": "qwen3.8-27b-q4:latest",
    ... etc ...
 curl http://localhost:8080/api/chat \
             -H "Content-Type: application/json" \
             -d '{
       "model": "qwen3.8-27b-q4:latest",
       "messages": [
         {
           "role": "user",
           "content": "Say hello in one sentence."
         }
       ],
       "stream": false
     }'
{"error":{"code":404,"message":"model \"qwen3.8-27b-q4:latest\" not found. To see available models, call GET /v1/models","type":"invalid_request_error"}}
 curl http://localhost:8080/api/chat \
             -H "Content-Type: application/json" \
             -d '{
       "model": "qwen3.8-27b-q4",
       "messages": [
         {
           "role": "user",
           "content": "Say hello in one sentence."
         }
       ],
       "stream": false
     }'
{"model":"qwen3.8-27b-q4","created_at":"2026-08-25T20:42:38.88581148Z","message":{"role":"assistant","content":"Hello!"},"done":true,"done_reason":"stop","total_duration":1736303182,"prompt_eval_count":58,"eval_count":37}
```
**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
Consistency across endpoints, so probably the /api/tags output should not include ":latest" 

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5755898e5732b227bc39239e870b4f856f3589fc`.  There
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
{"case_id": "mudler_LocalAI__11728__5755898",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
