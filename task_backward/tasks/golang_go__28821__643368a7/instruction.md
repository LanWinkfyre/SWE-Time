# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Go 1.12 breaks cgo

### What version of Go are you using (`go version`)?



### Does this issue reproduce with the latest release?

Not with go1.11.2, but with tip. 





cc @ianlancetaylor

### What operating system and processor architecture are you using (`go env`)?

```
$ ./bin/go env
GOARCH="amd64"
GOBIN=""
GOCACHE="/home/ivan/.cache/go-build"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="linux"
GOOS="linux"
GOPATH=""
GOPROXY=""
GORACE=""
GOROOT="/home/ivan/go"
GOTMPDIR=""
GOTOOLDIR="/home/ivan/go/pkg/tool/linux_amd64"
GCCGO="gccgo"
CC="gcc"
CXX="g++"
CGO_ENABLED="1"
GOMOD=""
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fmessage-length=0 -fdebug-prefix-map=/tmp/go-build395867230=/tmp/go-build -gno-record-gcc-switches"
```

### What did you do?

Run a Travic CI job that builds a CGO package:

* https://travis-ci.org/cloudflare/ebpf_exporter/jobs/455709945

### What did you expect to see?

Successfull compilation like on go1.11.2:

```
https://travis-ci.org/cloudflare/ebpf_exporter/jobs/455709944
```

### What did you see instead?

```
vendor/github.com/iovisor/gobpf/bcc/perf.go:191: cannot use _cgo5 (type int) as type _Ctype_int in argument to _C2func_bpf_open_perf_buffer
```

Code is [here](https://github.com/cloudflare/ebpf_exporter/blob/1fc0e67a43a8/vendor/github.com/iovisor/gobpf/bcc/perf.go#L191-L195):

```go
	reader, err := C.bpf_open_perf_buffer(
		(C.perf_reader_raw_cb)(unsafe.Pointer(C.callback_to_go)),
		nil,
		unsafe.Pointer(uintptr(callbackDataIndex)),
		-1, cpuC, BPF_PERF_READER_PAGE_CNT)
```
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `cb4130996fa7f73c62dafcd65a94233359fd9e09` and the full history behind it is present.
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
