# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
crypto/tls: TLS 1.3 handshake timeout with tip, Go 1.26 can connect successfully

<!-- Please answer these questions before submitting your issue. Thanks! -->

### What version of Go are you using (`go version`)?

<pre>
$ go version

</pre>

### Does this issue reproduce with the latest release?

No

### What operating system and processor architecture are you using (`go env`)?

<details><summary><code>go env</code> Output</summary><br><pre>
$ go env
AR='ar'
CC='clang'
CGO_CFLAGS='-O2 -g'
CGO_CPPFLAGS=''
CGO_CXXFLAGS='-O2 -g'
CGO_ENABLED='1'
CGO_FFLAGS='-O2 -g'
CGO_LDFLAGS='-O2 -g'
CXX='clang++'
GCCGO='gccgo'
GO111MODULE=''
GOARCH='arm64'
GOARM64='v8.0'
GOAUTH='netrc'
GOBIN=''
GOCACHE='/Users/kevin/Library/Caches/go-build'
GOCACHEPROG=''
GODEBUG=''
GOENV='/Users/kevin/Library/Application Support/go/env'
GOEXE=''
GOEXPERIMENT=''
GOFIPS140='off'
GOFLAGS=''
GOGCCFLAGS='-fPIC -arch arm64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -ffile-prefix-map=/var/folders/gh/xgxt3m8d5kd3353q6wyl6c1m0000gn/T/go-build927103055=/tmp/go-build -gno-record-gcc-switches -fno-common'
GOHOSTARCH='arm64'
GOHOSTOS='darwin'
GOINSECURE=''
GOMOD='/dev/null'
GOMODCACHE='/Users/kevin/pkg/mod'
GONOPROXY=''
GONOSUMDB=''
GOOS='darwin'
GOPACKAGESDRIVER=''
GOPATH='/Users/kevin'
GOPRIVATE=''
GOPROXY='direct'
GOROOT='/Users/kevin/go'
GOSUMDB='sum.golang.org'
GOTELEMETRY='local'
GOTELEMETRYDIR='/Users/kevin/Library/Application Support/go/telemetry'
GOTMPDIR=''
GOTOOLCHAIN='auto'
GOTOOLDIR='/Users/kevin/go/pkg/tool/darwin_arm64'
GOVCS=''

GOWORK=''
PKG_CONFIG='pkg-config'


uname -v: Darwin Kernel Version 25.3.0: Wed Jan 28 20:54:46 PST 2026; root:xnu-12377.91.3~2/RELEASE_ARM64_T6000
ProductName:		macOS
ProductVersion:		26.3.1
ProductVersionExtra:	(a)
BuildVersion:		25D771280a
lldb --version: lldb-2100.0.16.4
Apple Swift version 6.3 (swiftlang-6.3.0.123.5 clang-2100.0.123.102)
</pre></details>

### What did you do?

I can't connect to https://oakland.granicus.com/ with Go 1.27 at tip, it tries to negotiate TLS 1.3 and then just errors with "handshake timeout". 

Go 1.26 is able to complete a connection (as is my browser, curl, etc.)


 Here's the bisect script. 

```go
package main

import (
	"context"
	"io"
	"log/slog"
	"net/http"
	"os"
	"time"
)

const userAgent = "go-bisect-oakland-tls/0.1"

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stderr, nil))

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, "https://oakland.granicus.com", nil)
	if err != nil {
		logger.Error("create request", "err", err)
		os.Exit(2)
	}
	req.Header.Set("User-Agent", userAgent)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		logger.Error("request failed", "err", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	_, _ = io.Copy(io.Discard, io.LimitReader(resp.Body, 4096))
	logger.Info("request succeeded", "status", resp.Status)
}
```
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `5078670ed22e5b69c3b45d015333e5a1d58c8788` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
