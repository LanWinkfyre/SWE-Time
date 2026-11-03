# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/go: flag modcacherw does not take effect in the target package

### What version of Go are you using (`go version`)?

<pre>
$ go version
go version go1.21.4 linux/amd64
</pre>

### Does this issue reproduce with the latest release?

Yes

### What operating system and processor architecture are you using (`go env`)?

I tested this on a clean Debian container.

<details><summary><code>go env</code> Output</summary><br><pre>
$ go env
GO111MODULE=''
GOARCH='amd64'
GOBIN=''
GOCACHE='/root/.cache/go-build'
GOENV='/root/.config/go/env'
GOEXE=''
GOEXPERIMENT=''
GOFLAGS=''
GOHOSTARCH='amd64'
GOHOSTOS='linux'
GOINSECURE=''
GOMODCACHE='/root/go/pkg/mod'
GONOPROXY=''
GONOSUMDB=''
GOOS='linux'
GOPATH='/root/go'
GOPRIVATE=''
GOPROXY='https://proxy.golang.org,direct'
GOROOT='/usr/local/go'
GOSUMDB='sum.golang.org'
GOTMPDIR=''
GOTOOLCHAIN='auto'
GOTOOLDIR='/usr/local/go/pkg/tool/linux_amd64'
GOVCS=''
GOVERSION='go1.21.4'
GCCGO='gccgo'
GOAMD64='v1'
AR='ar'
CC='gcc'
CXX='g++'
CGO_ENABLED='0'
GOMOD='/dev/null'
GOWORK=''
CGO_CFLAGS='-O2 -g'
CGO_CPPFLAGS=''
CGO_CXXFLAGS='-O2 -g'
CGO_FFLAGS='-O2 -g'
CGO_LDFLAGS='-O2 -g'
PKG_CONFIG='pkg-config'
GOGCCFLAGS='-fPIC -m64 -fno-caret-diagnostics -Qunused-arguments -Wl,--no-gc-sections -fmessage-length=0 -ffile-prefix-map=/tmp/go-build392749006=/tmp/go-build -gno-record-gcc-switches'
</pre></details>

### What did you do?

1. Install a package using the `modcacherw` flag with `go install`:
   ```
   $ GOPATH=$(pwd)/_go go install -modcacherw github.com/google/go-containerregistry/cmd/crane@v0.16.1
   go: downloading github.com/google/go-containerregistry v0.16.1
   go: downloading github.com/docker/cli v24.0.0+incompatible
   go: downloading github.com/opencontainers/image-spec v1.1.0-rc3
   go: downloading github.com/spf13/cobra v1.7.0
   go: downloading github.com/opencontainers/go-digest v1.0.0
   go: downloading golang.org/x/sync v0.2.0
   go: downloading github.com/docker/distribution v2.8.2+incompatible
   go: downloading github.com/containerd/stargz-snapshotter/estargz v0.14.3
   go: downloading github.com/google/go-cmp v0.5.9
   go: downloading github.com/mitchellh/go-homedir v1.1.0
   go: downloading github.com/klauspost/compress v1.16.5
   go: downloading github.com/spf13/pflag v1.0.5
   go: downloading github.com/vbatts/tar-split v0.11.3
   go: downloading github.com/pkg/errors v0.9.1
   go: downloading golang.org/x/sys v0.8.0
   go: downloading github.com/docker/docker-credential-helpers v0.7.0
   go: downloading github.com/docker/docker v24.0.0+incompatible
   go: downloading github.com/sirupsen/logrus v1.9.1
   ```
1. List the directories:
   ```
   $ ls _go/pkg/mod/github.com/google/ -la
   total 16
   drwxr-xr-x  4 root root 4096 Nov 20 13:49 .
   drwxr-xr-x 12 root root 4096 Nov 20 13:49 ..
   drwxr-xr-x  4 root root 4096 Nov 20 13:49 go-cmp@v0.5.9
   dr-xr-xr-x 10 root root 4096 Nov 20 13:49 go-containerregistry@v0.16.1
   ```
1. Notice that `go-containerregistry@v0.16.1` has read only permissions while their dependencies (`go-cmp`) has read-write permissions, as expected.

### What did you expect to see?

I expected to see the directory `go-containerregistry@v0.16.1` to have read-write permissions, since I have set the flag `modcacherw`.

```
	-modcacherw
		leave newly-created directories in the module cache read-write
		instead of making them read-only.
```

### What did you see instead?

Instead `go-containerregistry@v0.16.1` has read only permissions.

I thinks this is a regression, since up to `v1.20` I confirmed that it worked as expected.
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `468bc941886ae83b8d16af5deaaf12ea5cabb05b` and the full history behind it is present.
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
