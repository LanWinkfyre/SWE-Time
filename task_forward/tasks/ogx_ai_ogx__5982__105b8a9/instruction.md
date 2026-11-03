# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
/v1/messages - support message role="system"

### 🚀 Describe the new functionality needed

support for input message with role="system"

### 💡 Why is this needed? What if we don't build it?

needed to use claude code cli

### Other thoughts

```
$ ANTHROPIC_BASE_URL=http://localhost:8321 ANTHROPIC_API_KEY=none claude
 ▐▛███▜▌   Claude Code v2.1.156
▝▜█████▛▘  Opus 4.8 (1M context) · API Usage Billing
  ▘▘ ▝▝    ...

   Opus 4.8 is here! Now defaults to high effort · /effort xhigh for your hardest tasks

❯ hello                                                                                                                                                                           
  ⎿  API Error: 400 {'errors': [{'loc': ['body', 'messages', 1, 'role'], 'msg': "Input should be 'user' or 'assistant'", 'type': 'literal_error'}]}

✻ Brewed for 0s  
```

```
Traceback (most recent call last):
  File ".../.venv/lib64/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File ".../.venv/lib64/python3.12/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File ".../.venv/lib64/python3.12/site-packages/fastapi/routing.py", line 723, in app
    raise validation_error
fastapi.exceptions.RequestValidationError: 1 validation error:
  {'type': 'literal_error', 'loc': ('body', 'messages', 1, 'role'), 'msg': "Input should be 'user' or 'assistant'", 'input': 'system', 'ctx': {'expected': "'user' or 'assistant'"}}

  File ".../src/ogx_api/messages/fastapi_routes.py", line 135, in create_message
    POST /v1/messages
INFO     2026-05-28T23:38:39.349377Z  ::1:54892 - "POST /v1/messages?beta=true HTTP/1.1" 400  category=server  
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `105b8a9e32bf49354f335ca94316284dd8b577be`.  There
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
{"case_id": "ogx_ai_ogx__5982__105b8a9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
