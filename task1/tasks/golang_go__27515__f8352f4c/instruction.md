# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/go: 'go build' fails when current directory and output directory are symlinks on Windows

## What version of Go are you using (`go version`)?

`go version go1.11 windows/amd64`

### Does this issue reproduce with the latest release?

Yes. This is a regression from go1.10.3.

### What operating system and processor architecture are you using (`go env`)?

Windows Server 1709 (OS Version 10.0.16299) and Windows Server 1803 (OS Version 10.0.17134). 

```
set GOARCH=amd64
set GOBIN=
set GOCACHE=C:\Users\Administrator\AppData\Local\go-build
set GOEXE=.exe
set GOFLAGS=
set GOHOSTARCH=amd64
set GOHOSTOS=windows
set GOOS=windows
set GOPATH=C:\Users\Administrator\go
set GOPROXY=
set GORACE=
set GOROOT=C:\Go
set GOTMPDIR=
set GOTOOLDIR=C:\Go\pkg\tool\windows_amd64
set GCCGO=gccgo
set CC=gcc
set CXX=g++
set CGO_ENABLED=1
set GOMOD=
set CGO_CFLAGS=-g -O2
set CGO_CPPFLAGS=
set CGO_CXXFLAGS=-g`<no output>` -O2
set CGO_FFLAGS=-g -O2
set CGO_LDFLAGS=-g -O2
set PKG_CONFIG=pkg-config
set GOGCCFLAGS=-m64 -mthreads -fmessage-length=0 -fdebug-prefix-map=C:\Users\Administrator\AppData\Local\Temp\go-build075376310=/tmp/go-build -gno-record-gcc-switches
```

### What did you do?

On Windows, create this directory structure.
```
C:\some-directory\
  hello\
  src\
  src2 [-> symlinked to C:\some-directory\src]
    hello [-> symlinked to C:\some-directory\hello]
    hello.go
```
From the directory `C:\some-directory\src2\`, run `go build -o c:\some-directory\src2\hello\hello.exe .\hello.go`.

### What did you expect to see?

The command succeeds and builds `hello.exe` in the directory `C:\some-directory\hello\`.

### What did you see instead?

```
go build command-line-arguments: mkdir C:\some-directory\src2\hello\: Cannot create a file when that file already exists.
```


I have used https://play.golang.org/p/xYnM-XHKDve to find the commit that broke the test:


It looks like cmd/go fails when it calls os.MkdirAll, which calls os.Stat of `C:\Users\Alex\AppData\Local\Temp\TestAlex496017355\src2\hello\` - note the backslash at the end of the path, and `C:\Users\Alex\AppData\Local\Temp\TestAlex496017355\src2` is the symlink. os.Stat of such directory succeeds on linux, and returns directory, but fails on windows.



If someone wants to have these 2 issues fixed, please, review https://golang.org/cl/134195 .

Alex
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `3c1b7bc7212cd894dae684ae064f4e7708b080ec` and the full history behind it is present.
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
