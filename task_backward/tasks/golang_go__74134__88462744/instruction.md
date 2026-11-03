# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/go: open C:\Windows\TEMP: Access is denied.

### Go version

go version go1.25rc1 windows/amd64

### Output of `go env` in your module/workspace:

```shell
set AR=ar
set CC=gcc
set CGO_CFLAGS=-O2 -g
set CGO_CPPFLAGS=
set CGO_CXXFLAGS=-O2 -g
set CGO_ENABLED=0
set CGO_FFLAGS=-O2 -g
set CGO_LDFLAGS=-O2 -g
set CXX=g++
set GCCGO=gccgo
set GO111MODULE=
set GOAMD64=v1
set GOARCH=amd64
set GOAUTH=netrc
set GOBIN=
set GOCACHE=C:\Users\ContainerUser\AppData\Local\go-build
set GOCACHEPROG=
set GODEBUG=
set GOENV=C:\Users\ContainerUser\AppData\Roaming\go\env
set GOEXE=.exe
set GOEXPERIMENT=
set GOFIPS140=off
set GOFLAGS=
set GOGCCFLAGS=-m64 -fno-caret-diagnostics -Qunused-arguments -Wl,--no-gc-sections -fmessage-length=0 -ffile-prefix-map=C:\Windows\TEMP\go-build662705847=/tmp/go-build -gno-record-gcc-switches
set GOHOSTARCH=amd64
set GOHOSTOS=windows
set GOINSECURE=
set GOMOD=NUL
set GOMODCACHE=C:\go\pkg\mod
set GONOPROXY=
set GONOSUMDB=
set GOOS=windows
set GOPATH=C:\go
set GOPRIVATE=
set GOPROXY=https://proxy.golang.org,direct
set GOROOT=C:\Program Files\Go
set GOSUMDB=sum.golang.org
set GOTELEMETRY=local
set GOTELEMETRYDIR=C:\Users\ContainerUser\AppData\Roaming\go\telemetry
set GOTMPDIR=
set GOTOOLCHAIN=auto
set GOTOOLDIR=C:\Program Files\Go\pkg\tool\windows_amd64
set GOVCS=
set GOVERSION=go1.25rc1
set GOWORK=
set PKG_CONFIG=pkg-config
```

### What did you do?

Running a build inside a fresh Windows Nano Server container which defaults to the unprivileged `ContainerUser` and `TMP` is set to `C:\Windows\TEMP`: commands such as `go build` and `go run` fail to clean up from `C:\Windows\Temp` with `go: open C:\Windows\TEMP: Access is denied.`

```go
package main

import "fmt"

func main() {
	fmt.Printf("Hello World!\n")
}
```

(saved as `hello.go`)

### What did you see happen?

```console
C:\go>go build -o hello.exe hello.go
go: open C:\Windows\TEMP: Access is denied.
```

### What did you expect to see?

When I do the same exact process with Go 1.24, it works fine without errors.

See also https://github.com/docker-library/golang/issues/563, especially https://github.com/docker-library/golang/issues/563#issuecomment-2968325383 -- I bisected this and got the following:





 🙈
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `934d5f2cf703c6aad9f0ce6a73a3922d1af83049` and the full history behind it is present.
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
