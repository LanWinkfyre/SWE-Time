# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
debug/elf: infinite loop? in elf.NewFile (recent regression from go 1.19)

<!-- Please answer these questions before submitting your issue. Thanks! -->

### What version of Go are you using (`go version`)?

<pre>
$ go version
go version go1.18.3 darwin/amd64
</pre>

### Does this issue reproduce with the latest release?


### What operating system and processor architecture are you using (`go env`)?

<details><summary><code>go env</code> Output</summary><br><pre>
$ go env
GO111MODULE=""
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/catena/Library/Caches/go-build"
GOENV="/Users/catena/Library/Application Support/go/env"
GOEXE=""
GOEXPERIMENT=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOINSECURE=""
GOMODCACHE="/Users/catena/go/pkg/mod"
GONOPROXY=""
GONOSUMDB=""
GOOS="darwin"
GOPATH="/Users/catena/go"
GOPRIVATE=""
GOPROXY="https://proxy.golang.org,direct"
GOROOT="/usr/local/go"
GOSUMDB="sum.golang.org"
GOTMPDIR=""
GOTOOLDIR="/usr/local/go/pkg/tool/darwin_amd64"
GOVCS=""
GOVERSION="go1.18.3"
GCCGO="gccgo"
GOAMD64="v1"
AR="ar"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD="/dev/null"
GOWORK=""
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -arch x86_64 -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/pp/dc1dtf9x2js3v0jx_m010nqr0000gn/T/go-build2205394633=/tmp/go-build -gno-record-gcc-switches -fno-common"
GOROOT/bin/go version: go version go1.18.3 darwin/amd64
GOROOT/bin/go tool compile -V: compile version go1.18.3
uname -v: Darwin Kernel Version 21.6.0: Mon Aug 22 20:17:10 PDT 2022; root:xnu-8020.140.49~2/RELEASE_X86_64
ProductName:	macOS
ProductVersion:	12.6
BuildVersion:	21G115
lldb --version: lldb-1400.0.30.3
Apple Swift version 5.7 (swiftlang-5.7.0.127.4 clang-1400.0.29.50)
gdb --version: GNU gdb (GDB) 12.1
</pre></details>

### What did you do?

Run https://go.dev/play/p/43zIUU90Ko9?v=gotip

No problem on go 1.19 cf https://go.dev/play/p/43zIUU90Ko9

### What did you expect to see?

The program printing Hello

### What did you see instead?

```

Program exited.
```

Found by ngolo-fuzzing https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=52297
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `213504e5431891e8421a92ab72ac08981ce07516` and the full history behind it is present.
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
