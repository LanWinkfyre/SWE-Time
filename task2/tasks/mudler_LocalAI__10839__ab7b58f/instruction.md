# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 1: Unauthenticated race condition in P2P settings update causes denial of service

**LocalAI version:**
commit `05b8d8aafe91401938622e1759c7dbf9425c8a95` (master, 2026-07-14)

**Environment, CPU architecture, OS, and Version:**
Linux 6.8.0-55-generic, x86_64, Docker container built with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`core/application/p2p.go` mutates `Application.p2pCtx`/`p2pCancel` with inconsistent locking. `StopP2P()` reads and writes both fields without taking `a.p2pMutex`. `RestartP2P()` holds the mutex only around the old context's cancel, then spawns a background goroutine calling `StartP2P()`, which reassigns the same fields at `p2p.go:40-41` with no lock at all.

Both paths are reachable from `POST /api/settings`: an empty `p2p_token` triggers `StopP2P()`, a non-empty one triggers `RestartP2P()` (`core/http/endpoints/localai/settings.go:291-311`). Concurrent requests race on the same struct fields, a data race (CWE-362).

The route needs no authentication by default, `adminMiddleware` resolves to `auth.NoopMiddleware()` when no `--api-keys`/auth DB is configured (`core/http/app.go:375-381`).

**To Reproduce**

Build a `-race` instrumented LocalAI image and run it, then hammer `POST /api/settings` concurrently.

```bash
# 1. Clone and build a race-instrumented local-ai binary in a minimal image
git clone --depth 1 https://github.com/mudler/LocalAI.git /tmp/localai-race
cd /tmp/localai-race

cat > Dockerfile.race <<'EOF'
FROM golang:1.23-bookworm AS build
WORKDIR /src
COPY . .
RUN go build -race -o /usr/local/bin/local-ai ./cmd/local-ai

FROM debian:bookworm-slim
COPY --from=build /usr/local/bin/local-ai /usr/local/bin/local-ai
ENTRYPOINT ["/usr/local/bin/local-ai"]
EOF

docker build -t localai-race:latest -f Dockerfile.race .

# 2. Start the victim with no auth configured, so /api/settings is unauthenticated
mkdir -p /tmp/localai-race-models
docker run -d --rm --name localai-race-victim \
    -p 8080:8080 \
    -v /tmp/localai-race-models:/models \
    localai-race:latest run \
    --address 0.0.0.0:8080 \
    --models-path /models \
    --api-keys ""

# 3. Wait for readiness
until curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/readyz | grep -q 200; do sleep 1; done

# 4. Fire many concurrent POST /api/settings requests that alternate
#    setting a P2P token (-> RestartP2P) and clearing it (-> StopP2P)
for w in 1 2 3 4 5 6; do
  (
    for n in $(seq 1 15); do
      if [ $(( (n + w) % 2 )) -eq 0 ]; then
        body="{\"p2p_token\":\"race-token-${w}-${n}\",\"p2p_network_id\":\"auditnet-${w}\"}"
      else
        body='{"p2p_token":""}'
      fi
      curl -s -o /dev/null -H "Content-Type: application/json" \
        -X POST -d "$body" http://127.0.0.1:8080/api/settings
    done
  ) &
done
wait

# 5. Inspect the container logs for the race detector report
docker logs localai-race-victim 2>&1 | grep -A 40 "WARNING: DATA RACE"
```

**Expected behavior**

Concurrent `POST /api/settings` requests should serialize access to `Application.p2pCtx`/`p2pCancel`, no data race should occur regardless of request timing.

**Logs**

```
WARNING: DATA RACE
Read at 0x00c001487c88 by goroutine 311:
  github.com/mudler/LocalAI/core/application.(*Application).StopP2P()
      /src/core/application/p2p.go:21 +0x3b
  github.com/mudler/LocalAI/core/http/routes.RegisterUIAPIRoutes.UpdateSettingsEndpoint.func32()
      /src/core/http/endpoints/localai/settings.go:295 +0x2289
  ... (echo middleware chain) ...
  net/http.(*conn).serve()
      /usr/local/go/src/net/http/server.go:2073 +0xda4

Previous write at 0x00c001487c88 by goroutine 310:
  github.com/mudler/LocalAI/core/application.(*Application).RestartP2P()
      /src/core/application/p2p.go:136 +0x10a
  github.com/mudler/LocalAI/core/http/routes.RegisterUIAPIRoutes.UpdateSettingsEndpoint.func32()
      /src/core/http/endpoints/localai/settings.go:303 +0x2452
  ... (echo middleware chain) ...
  net/http.(*conn).serve()
      /usr/local/go/src/net/http/server.go:2073 +0xda4

Goroutine 311 (running) created at:
  net/http.(*Server).Serve()
      /usr/local/go/src/net/http/server.go:3464 +0x889
  github.com/labstack/echo/v4.(*Echo).Start()
      /go/pkg/mod/github.com/labstack/echo/v4@v4.15.1/echo.go:693 +0x144
  main.main()
      /src/cmd/local-ai/main.go:107 +0x10a4

Goroutine 310 (running) created at:
  net/http.(*Server).Serve()
      /usr/local/go/src/net/http/server.go:3464 +0x889
  github.com/labstack/echo/v4.(*Echo).Start()
      /go/pkg/mod/github.com/labstack/echo/v4@v4.15.1/echo.go:693 +0x144
  main.main()
      /src/cmd/local-ai/main.go:107 +0x10a4
```

The race is a read of `p2pCancel` in `StopP2P` (p2p.go:21) against a concurrent write in `RestartP2P` (p2p.go:136), exactly the two functions and fields described above. Captured by rerunning the PoC on 2026-07-15 against the existing `localai-audit:latest` race-instrumented image.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ab7b58fc85a21c559ba3a26d521792dc0e037c66`.  There
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
{"case_id": "mudler_LocalAI__10839__ab7b58f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
