# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime/checkptr: fatal error: checkptr: pointer arithmetic result points to invalid allocation

### Go version

`go version go1.23rc1 darwin/arm64`

### Output of `go env` in your module/workspace:

```shell
GO111MODULE=''
GOARCH='arm64'
GOBIN=''
GOCACHE='/Users/xxx/Library/Caches/go-build'
GOENV='/Users/xxx/Library/Application Support/go/env'
GOEXE=''
GOEXPERIMENT='arenas'
GOFLAGS=''
GOHOSTARCH='arm64'
GOHOSTOS='darwin'
GOINSECURE=''
GOMODCACHE='/Users/xxx/go/pkg/mod'
GOOS='darwin'
GOPATH='/Users/xxx/go'
GOPROXY='https://goproxy.cn'
GOROOT='/Users/xxx/sdk/go1.23rc1'
GOSUMDB='sum.golang.org'
GOTMPDIR=''
GOTOOLCHAIN='auto'
GOTOOLDIR='/Users/xxx/sdk/go1.23rc1/pkg/tool/darwin_arm64'
GOVCS=''
GOVERSION='go1.23rc1'
GODEBUG=''
GOTELEMETRY='local'
GOTELEMETRYDIR='/Users/xxx/Library/Application Support/go/telemetry'
GCCGO='gccgo'
GOARM64='v8.0'
AR='ar'
CC='clang'
CXX='clang++'
CGO_ENABLED='1'
GOMOD='/dev/null'
GOWORK=''
CGO_CFLAGS='-O2 -g'
CGO_CPPFLAGS=''
CGO_CXXFLAGS='-O2 -g'
CGO_FFLAGS='-O2 -g'
CGO_LDFLAGS='-O2 -g'
PKG_CONFIG='pkg-config'
GOGCCFLAGS='-fPIC -arch arm64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -ffile-prefix-map=/var/folders/df/2vy1kgkn1_98kqwtn0zgdyj80000gn/T/go-build775107601=/tmp/go-build -gno-record-gcc-switches -fno-common'
```


### What did you do?

Run the following program with `-gcflags=all=-d=checkptr` flag.

```go
package main

import "regexp"

var dataFileRegexp = regexp.MustCompile(`^data\.\d+\.bin$`)

func main() {
	_ = dataFileRegexp
}
```

### What did you see happen?

```
fatal error: checkptr: pointer arithmetic result points to invalid allocation

goroutine 1 gp=0x140000021c0 m=0 mp=0x100cfd640 [running, locked to thread]:
runtime.throw({0x100c5465d?, 0x100c4bb34?})
	/Users/xxx/sdk/go1.23rc1/src/runtime/panic.go:1067 +0x38 fp=0x14000078bf0 sp=0x14000078bc0 pc=0x100c27678
runtime.checkptrArithmetic(0x1400007c180?, {0x0, 0x0, 0x80?})
	/Users/xxx/sdk/go1.23rc1/src/runtime/checkptr.go:69 +0xa8 fp=0x14000078c20 sp=0x14000078bf0 pc=0x100bcd568
internal/abi.NoEscape(...)
	/Users/xxx/sdk/go1.23rc1/src/internal/abi/escape.go:21
strings.(*Builder).copyCheck(...)
	/Users/xxx/sdk/go1.23rc1/src/strings/builder.go:33
strings.(*Builder).WriteRune(0x14000078cb8, 0x64)
	/Users/xxx/sdk/go1.23rc1/src/strings/builder.go:98 +0x48 fp=0x14000078c80 sp=0x14000078c20 pc=0x100c38588
regexp.onePassPrefix(0x1400007c120)
	/Users/xxx/sdk/go1.23rc1/src/regexp/onepass.go:60 +0x170 fp=0x14000078ce0 sp=0x14000078c80 pc=0x100c49450
regexp.compile({0x100c4f3ee, 0x10}, 0xd640?, 0x0)
	/Users/xxx/sdk/go1.23rc1/src/regexp/regexp.go:203 +0x208 fp=0x14000078d70 sp=0x14000078ce0 pc=0x100c4bee8
regexp.Compile(...)
	/Users/xxx/sdk/go1.23rc1/src/regexp/regexp.go:135
regexp.MustCompile({0x100c4f3ee, 0x10})
	/Users/xxx/sdk/go1.23rc1/src/regexp/regexp.go:315 +0x30 fp=0x14000078df0 sp=0x14000078d70 pc=0x100c4c3b0
main.init()
	/Users/xxx/Projects/guance/local-dev/cmd/checkptr/main.go:5 +0x28 fp=0x14000078e10 sp=0x14000078df0 pc=0x100c4d758
runtime.doInit1(0x100ce8820)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:7278 +0xd4 fp=0x14000078f40 sp=0x14000078e10 pc=0x100c082b4
runtime.doInit(...)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:7245
runtime.main()
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:254 +0x344 fp=0x14000078fd0 sp=0x14000078f40 pc=0x100bf90d4
runtime.goexit({})
	/Users/xxx/sdk/go1.23rc1/src/runtime/asm_arm64.s:1223 +0x4 fp=0x14000078fd0 sp=0x14000078fd0 pc=0x100c2dac4

goroutine 2 gp=0x14000002700 m=nil [force gc (idle)]:
runtime.gopark(0x0?, 0x0?, 0x0?, 0x0?, 0x0?)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:424 +0xc8 fp=0x1400004ef90 sp=0x1400004ef70 pc=0x100c27758
runtime.goparkunlock(...)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:430
runtime.forcegchelper()
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:337 +0xb8 fp=0x1400004efd0 sp=0x1400004ef90 pc=0x100bf9378
runtime.goexit({})
	/Users/xxx/sdk/go1.23rc1/src/runtime/asm_arm64.s:1223 +0x4 fp=0x1400004efd0 sp=0x1400004efd0 pc=0x100c2dac4
created by runtime.init.7 in goroutine 1
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:325 +0x24

goroutine 17 gp=0x14000082380 m=nil [GC sweep wait]:
runtime.gopark(0x0?, 0x0?, 0x0?, 0x0?, 0x0?)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:424 +0xc8 fp=0x1400004a760 sp=0x1400004a740 pc=0x100c27758
runtime.goparkunlock(...)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:430
runtime.bgsweep(0x1400008e000)
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgcsweep.go:277 +0xa0 fp=0x1400004a7b0 sp=0x1400004a760 pc=0x100be5cb0
runtime.gcenable.gowrap1()
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgc.go:203 +0x28 fp=0x1400004a7d0 sp=0x1400004a7b0 pc=0x100bd9f38
runtime.goexit({})
	/Users/xxx/sdk/go1.23rc1/src/runtime/asm_arm64.s:1223 +0x4 fp=0x1400004a7d0 sp=0x1400004a7d0 pc=0x100c2dac4
created by runtime.gcenable in goroutine 1
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgc.go:203 +0x6c

goroutine 18 gp=0x14000082540 m=nil [GC scavenge wait]:
runtime.gopark(0x1400008e000?, 0x100c6d020?, 0x1?, 0x0?, 0x14000082540?)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:424 +0xc8 fp=0x1400004af60 sp=0x1400004af40 pc=0x100c27758
runtime.goparkunlock(...)
	/Users/xxx/sdk/go1.23rc1/src/runtime/proc.go:430
runtime.(*scavengerState).park(0x100cfcec0)
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgcscavenge.go:425 +0x5c fp=0x1400004af90 sp=0x1400004af60 pc=0x100be36ac
runtime.bgscavenge(0x1400008e000)
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgcscavenge.go:653 +0x44 fp=0x1400004afb0 sp=0x1400004af90 pc=0x100be3bf4
runtime.gcenable.gowrap2()
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgc.go:204 +0x28 fp=0x1400004afd0 sp=0x1400004afb0 pc=0x100bd9ed8
runtime.goexit({})
	/Users/xxx/sdk/go1.23rc1/src/runtime/asm_arm64.s:1223 +0x4 fp=0x1400004afd0 sp=0x1400004afd0 pc=0x100c2dac4
created by runtime.gcenable in goroutine 1
	/Users/xxx/sdk/go1.23rc1/src/runtime/mgc.go:204 +0xac
exit status 2
```

### What did you expect to see?

Normal exit like using go1.22.

I reproduced the issue on `linux/amd64`. 
cc @mknyszek @dr2chase
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `071b8d51c1a70fa6b12f0bed2e93370e193333fd` and the full history behind it is present.
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
