# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
net/http/httputil: all goroutines are asleep - deadlock

### What version of Go are you using (`go version`)?



### What operating system and processor architecture are you using (`go env`)?

set GOARCH=amd64
set GOBIN=
set GOEXE=.exe
set GOHOSTARCH=amd64
set GOHOSTOS=windows
set GOOS=windows
set GOPATH=d:\a
set GORACE=
set GOROOT=d:\a\go
set GOTOOLDIR=d:\a\go\pkg\tool\windows_amd64
set GCCGO=gccgo
set CC=gcc
set GOGCCFLAGS=-m64 -mthreads -fmessage-length=0 -fdebug-prefix-map=C:\Users\brainman\AppData\Local\Temp\1\go-build025530391=/tmp/go-build -gno-record-gcc-switches
set CXX=g++
set CGO_ENABLED=1
set CGO_CFLAGS=-g -O2
set CGO_CPPFLAGS=
set CGO_CXXFLAGS=-g -O2
set CGO_FFLAGS=-g -O2
set CGO_LDFLAGS=-g -O2
set PKG_CONFIG=pkg-config

### What did you do?

I run
```
go test -short net/http/httputil
```
command.

### What did you expect to see?

I expected test to PASS.

### What did you see instead?

```
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan receive]:
testing.(*T).Run(0xc0420fe000, 0x72d0ab, 0x10, 0x740778, 0x482701)
	d:/a/go/src/testing/testing.go:790 +0x303
testing.runTests.func1(0xc0420fe000)
	d:/a/go/src/testing/testing.go:1004 +0x73
testing.tRunner(0xc0420fe000, 0xc042057de8)
	d:/a/go/src/testing/testing.go:747 +0xd7
testing.runTests(0xc0420c0720, 0x8c15a0, 0xf, 0xf, 0x4)
	d:/a/go/src/testing/testing.go:1002 +0x1fd
testing.(*M).Run(0xc042057f20, 0xc042057f78)
	d:/a/go/src/testing/testing.go:921 +0x118
main.main()
	net/http/httputil/_test/_testmain.go:84 +0xe2

goroutine 27 [select]:
net/http.(*persistConn).roundTrip(0xc04207b9e0, 0xc0421788a0, 0x0, 0x0, 0x0)
	d:/a/go/src/net/http/transport.go:1962 +0x659
net/http.(*Transport).RoundTrip(0xc0420fe960, 0xc0420dd300, 0xc0420fe960, 0x0, 0x0)
	d:/a/go/src/net/http/transport.go:408 +0x853
net/http.send(0xc0420dd300, 0x88bf80, 0xc0420fe960, 0x0, 0x0, 0x0, 0xc042004108, 0x71f380, 0xc04202faa8, 0x1)
	d:/a/go/src/net/http/client.go:249 +0x1b0
net/http.(*Client).send(0xc042065920, 0xc0420dd300, 0x0, 0x0, 0x0, 0xc042004108, 0x0, 0x1, 0x41159f)
	d:/a/go/src/net/http/client.go:173 +0x10e
net/http.(*Client).Do(0xc042065920, 0xc0420dd300, 0xc04200a420, 0x23, 0x0)
	d:/a/go/src/net/http/client.go:598 +0x1fc
net/http/httputil.TestReverseProxy(0xc0420fe780)
	d:/a/go/src/net/http/httputil/reverseproxy_test.go:130 +0xce3
testing.tRunner(0xc0420fe780, 0x740778)
	d:/a/go/src/testing/testing.go:747 +0xd7
created by testing.(*T).Run
	d:/a/go/src/testing/testing.go:789 +0x2e5

goroutine 28 [IO wait]:
internal/poll.runtime_pollWait(0x27f4f00, 0x72, 0xc04207eb58)
	d:/a/go/src/runtime/netpoll.go:173 +0x77
internal/poll.(*pollDesc).wait(0xc04207ec98, 0x72, 0x88a400, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_poll_runtime.go:85 +0xb5
internal/poll.(*ioSrv).ExecIO(0x8c3c40, 0xc04207eb58, 0x72a763, 0x8, 0xc0420c1620, 0x2, 0x1, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:191 +0x126
internal/poll.(*FD).acceptOne(0xc04207eb40, 0xa0, 0xc0420c2540, 0x2, 0x2, 0xc04207eb58, 0x8, 0xc042115d28, 0x41159f, 0x10)
	d:/a/go/src/internal/poll/fd_windows.go:731 +0xc9
internal/poll.(*FD).Accept(0xc04207eb40, 0xc042031b90, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, ...)
	d:/a/go/src/internal/poll/fd_windows.go:765 +0x14f
net.(*netFD).accept(0xc04207eb40, 0xc042115ea8, 0x40110e, 0xc04203cc60)
	d:/a/go/src/net/fd_windows.go:191 +0x88
net.(*TCPListener).accept(0xc042004088, 0x64c947, 0x459900, 0xc042115ef0)
	d:/a/go/src/net/tcpsock_posix.go:136 +0x35
net.(*TCPListener).Accept(0xc042004088, 0x740498, 0xc04203cbe0, 0x890800, 0xc042065c50)
	d:/a/go/src/net/tcpsock.go:228 +0x50
net/http.(*Server).Serve(0xc04206e2c0, 0x8900c0, 0xc042004088, 0x0, 0x0)
	d:/a/go/src/net/http/server.go:2656 +0x27b
net/http/httptest.(*Server).goServe.func1(0xc0421009a0)
	d:/a/go/src/net/http/httptest/server.go:277 +0x74
created by net/http/httptest.(*Server).goServe
	d:/a/go/src/net/http/httptest/server.go:275 +0x63

goroutine 46 [IO wait]:
internal/poll.runtime_pollWait(0x27f4d80, 0x72, 0x0)
	d:/a/go/src/runtime/netpoll.go:173 +0x77
internal/poll.(*pollDesc).wait(0xc04207fa18, 0x72, 0x88a400, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_poll_runtime.go:85 +0xb5
internal/poll.(*ioSrv).ExecIO(0x8c3c40, 0xc04207f8d8, 0x72a5a2, 0x7, 0x7402b0, 0x0, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:191 +0x126
internal/poll.(*FD).Read(0xc04207f8c0, 0xc04218f000, 0x1000, 0x1000, 0x0, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:422 +0x285
net.(*netFD).Read(0xc04207f8c0, 0xc04218f000, 0x1000, 0x1000, 0x200000003, 0xc04201d800, 0xc042165a88)
	d:/a/go/src/net/fd_windows.go:150 +0x59
net.(*conn).Read(0xc042004110, 0xc04218f000, 0x1000, 0x1000, 0x0, 0x0, 0x0)
	d:/a/go/src/net/net.go:176 +0x74
net/http.(*persistConn).Read(0xc04207b9e0, 0xc04218f000, 0x1000, 0x1000, 0x0, 0x0, 0xc042165b68)
	d:/a/go/src/net/http/transport.go:1373 +0x147
bufio.(*Reader).fill(0xc042037e00)
	d:/a/go/src/bufio/bufio.go:97 +0x10f
bufio.(*Reader).Peek(0xc042037e00, 0x1, 0xc042039ec0, 0xc042165c80, 0x8c62c0, 0x8c62c0, 0x42fe51)
	d:/a/go/src/bufio/bufio.go:129 +0x53
net/http.(*persistConn).readLoop(0xc04207b9e0)
	d:/a/go/src/net/http/transport.go:1521 +0x189
created by net/http.(*Transport).dialConn
	d:/a/go/src/net/http/transport.go:1168 +0xa35

goroutine 50 [select]:
net/http/httputil.(*ReverseProxy).ServeHTTP.func1(0xc0420342a0, 0xc0420319b0, 0x890740, 0xc042033600)
	d:/a/go/src/net/http/httputil/reverseproxy.go:144 +0xf9
created by net/http/httputil.(*ReverseProxy).ServeHTTP
	d:/a/go/src/net/http/httputil/reverseproxy.go:143 +0xec4

goroutine 47 [select]:
net/http.(*persistConn).writeLoop(0xc04207b9e0)
	d:/a/go/src/net/http/transport.go:1751 +0x2ba
created by net/http.(*Transport).dialConn
	d:/a/go/src/net/http/transport.go:1169 +0xa5a

goroutine 29 [IO wait]:
internal/poll.runtime_pollWait(0x27f4e40, 0x72, 0xc04207ed98)
	d:/a/go/src/runtime/netpoll.go:173 +0x77
internal/poll.(*pollDesc).wait(0xc04207eed8, 0x72, 0x88a400, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_poll_runtime.go:85 +0xb5
internal/poll.(*ioSrv).ExecIO(0x8c3c40, 0xc04207ed98, 0x72a763, 0x8, 0xc0420c15c0, 0x2, 0x1, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:191 +0x126
internal/poll.(*FD).acceptOne(0xc04207ed80, 0xa4, 0xc0420c2460, 0x2, 0x2, 0xc04207ed98, 0x8, 0xc042113d28, 0x41159f, 0x10)
	d:/a/go/src/internal/poll/fd_windows.go:731 +0xc9
internal/poll.(*FD).Accept(0xc04207ed80, 0xc042031980, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, ...)
	d:/a/go/src/internal/poll/fd_windows.go:765 +0x14f
net.(*netFD).accept(0xc04207ed80, 0xc042113ea8, 0x40110e, 0xc04203cbc0)
	d:/a/go/src/net/fd_windows.go:191 +0x88
net.(*TCPListener).accept(0xc042004090, 0x64c947, 0x459900, 0xc042113ef0)
	d:/a/go/src/net/tcpsock_posix.go:136 +0x35
net.(*TCPListener).Accept(0xc042004090, 0x740498, 0xc04203cb40, 0x890800, 0xc042065d10)
	d:/a/go/src/net/tcpsock.go:228 +0x50
net/http.(*Server).Serve(0xc04206e370, 0x8900c0, 0xc042004090, 0x0, 0x0)
	d:/a/go/src/net/http/server.go:2656 +0x27b
net/http/httptest.(*Server).goServe.func1(0xc042100a10)
	d:/a/go/src/net/http/httptest/server.go:277 +0x74
created by net/http/httptest.(*Server).goServe
	d:/a/go/src/net/http/httptest/server.go:275 +0x63

goroutine 48 [select]:
net/http.(*persistConn).roundTrip(0xc04207bb00, 0xc042178d20, 0x0, 0x0, 0x0)
	d:/a/go/src/net/http/transport.go:1962 +0x659
net/http.(*Transport).RoundTrip(0x8c1240, 0xc0420dd500, 0xf, 0xc04200eaf0, 0x9)
	d:/a/go/src/net/http/transport.go:408 +0x853
net/http/httputil.(*ReverseProxy).ServeHTTP(0xc042032c80, 0x890240, 0xc0421741c0, 0xc0420dd400)
	d:/a/go/src/net/http/httputil/reverseproxy.go:203 +0x2b9
net/http.serverHandler.ServeHTTP(0xc04206e370, 0x890240, 0xc0421741c0, 0xc0420dd400)
	d:/a/go/src/net/http/server.go:2580 +0xbb
net/http.(*conn).serve(0xc04203cb40, 0x890740, 0xc042033500)
	d:/a/go/src/net/http/server.go:1797 +0x6a8
created by net/http.(*Server).Serve
	d:/a/go/src/net/http/server.go:2681 +0x257

goroutine 49 [IO wait]:
internal/poll.runtime_pollWait(0x27f4cc0, 0x72, 0x0)
	d:/a/go/src/runtime/netpoll.go:173 +0x77
internal/poll.(*pollDesc).wait(0xc04207fc58, 0x72, 0x88a400, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_poll_runtime.go:85 +0xb5
internal/poll.(*ioSrv).ExecIO(0x8c3c40, 0xc04207fb18, 0x72a5a2, 0x7, 0x7402b0, 0x0, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:191 +0x126
internal/poll.(*FD).Read(0xc04207fb00, 0xc042178ac1, 0x1, 0x1, 0x0, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:422 +0x285
net.(*netFD).Read(0xc04207fb00, 0xc042178ac1, 0x1, 0x1, 0x0, 0x0, 0x0)
	d:/a/go/src/net/fd_windows.go:150 +0x59
net.(*conn).Read(0xc042004118, 0xc042178ac1, 0x1, 0x1, 0x0, 0x0, 0x0)
	d:/a/go/src/net/net.go:176 +0x74
net/http.(*connReader).backgroundRead(0xc042178ab0)
	d:/a/go/src/net/http/server.go:656 +0x69
created by net/http.(*connReader).startBackgroundRead
	d:/a/go/src/net/http/server.go:652 +0xdb

goroutine 55 [select]:
net/http.(*persistConn).writeLoop(0xc04207bb00)
	d:/a/go/src/net/http/transport.go:1751 +0x2ba
created by net/http.(*Transport).dialConn
	d:/a/go/src/net/http/transport.go:1169 +0xa5a

goroutine 54 [IO wait]:
internal/poll.runtime_pollWait(0x27f4c00, 0x72, 0x0)
	d:/a/go/src/runtime/netpoll.go:173 +0x77
internal/poll.(*pollDesc).wait(0xc04207fe98, 0x72, 0x88a400, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_poll_runtime.go:85 +0xb5
internal/poll.(*ioSrv).ExecIO(0x8c3c40, 0xc04207fd58, 0x72a5a2, 0x7, 0x7402b0, 0x200000003, 0xc04201de00, 0xc0421619c0)
	d:/a/go/src/internal/poll/fd_windows.go:191 +0x126
internal/poll.(*FD).Read(0xc04207fd40, 0xc0421a0000, 0x1000, 0x1000, 0x0, 0x0, 0x0)
	d:/a/go/src/internal/poll/fd_windows.go:422 +0x285
net.(*netFD).Read(0xc04207fd40, 0xc0421a0000, 0x1000, 0x1000, 0x0, 0x0, 0x27f4b40)
	d:/a/go/src/net/fd_windows.go:150 +0x59
net.(*conn).Read(0xc042004120, 0xc0421a0000, 0x1000, 0x1000, 0x0, 0x0, 0x0)
	d:/a/go/src/net/net.go:176 +0x74
net/http.(*persistConn).Read(0xc04207bb00, 0xc0421a0000, 0x1000, 0x1000, 0x0, 0x0, 0xc042161b68)
	d:/a/go/src/net/http/transport.go:1373 +0x147
bufio.(*Reader).fill(0xc04219e120)
	d:/a/go/src/bufio/bufio.go:97 +0x10f
bufio.(*Reader).Peek(0xc04219e120, 0x1, 0xc04219c420, 0xc042161c80, 0x4126b2, 0xc042119048, 0x0)
	d:/a/go/src/bufio/bufio.go:129 +0x53
net/http.(*persistConn).readLoop(0xc04207bb00)
	d:/a/go/src/net/http/transport.go:1521 +0x189
created by net/http.(*Transport).dialConn
	d:/a/go/src/net/http/transport.go:1168 +0xa35
FAIL	net/http/httputil	0.104s
```

Sometimes test passes and sometimes it fails.

Alex




Alex
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `fca6ad45e25647d8d156a8ecd29137000408efeb` and the full history behind it is present.
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
