# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 3: Invalid `cutstrings` regex kills the LocalAI process through chat completions

**LocalAI version:**
commit `05b8d8aafe91401938622e1759c7dbf9425c8a95` (master, 2026-07-14)

**Environment, CPU architecture, OS, and Version:**
Linux 6.8.0-55-generic, x86_64, Docker container. Not architecture specific.

**Describe the bug**

`core/backend/llm.go` compiles every model `cutstrings` entry during response post-processing. If a regex is invalid, the error path calls `xlog.Fatal`, which terminates the entire `local-ai` process. A model file with `cutstrings: ["("]` can therefore turn one normal `/v1/chat/completions` request into a process-level denial of service.

**To Reproduce**

```bash
mkdir -p /tmp/localai-llm-fatal/models
cd /tmp/localai-llm-fatal

cat > models/model.yaml <<'EOF'
name: mock-model
backend: mock-backend
parameters:
  model: mock-model.bin
cutstrings:
  - "("
EOF

cat > payload.json <<'EOF'
{
  "model": "mock-model",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
EOF

docker rm -f localai-llm-fatal >/dev/null 2>&1 || true
docker run -d --name localai-llm-fatal \
  -p 8080:8080 \
  -v /tmp/localai-llm-fatal/models:/models \
  localai-audit:latest run \
  --address 0.0.0.0:8080 \
  --models-path /models \
  --api-keys "" \
  --external-grpc-backends "mock-backend:/usr/local/bin/mock-backend"

until curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/readyz | grep -q 200; do sleep 1; done

docker inspect -f '{{.State.Status}} exitcode={{.State.ExitCode}}' localai-llm-fatal
curl -sS -m 20 http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @payload.json
echo
sleep 3
docker inspect -f '{{.State.Status}} exitcode={{.State.ExitCode}}' localai-llm-fatal
curl -sS -m 5 http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @payload.json
docker logs localai-llm-fatal 2>&1 | tail -80
docker rm -f localai-llm-fatal >/dev/null 2>&1 || true
```

**Expected behavior**

Invalid model regex configuration should reject the model or return a request error. It should not terminate the LocalAI process.

**Logs**

```
--- before request: container status ---
running exitcode=0
--- sending first request ---
curl: (52) Empty reply from server
curl exit=52
--- after request: container status ---
exited exitcode=1
--- attempting a second request ---
curl: (7) Failed to connect to 127.0.0.1 port 32908 after 0 ms: Couldn't connect to server
Jul 14 15:42:52 ERROR failed to compile regex error=error parsing regexp: missing closing ): `(`
--- final container status ---
exited exitcode=1
```

**Additional context**

The crash happens after the backend returns and LocalAI applies model post-processing. The mock backend is enough to reach the vulnerable path.
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
{"case_id": "mudler_LocalAI__10843__a23fcc9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
