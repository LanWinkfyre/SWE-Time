# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
reflect: multiple "reflect" packages results in "invalid memory address or nil pointer dereference"

Please answer these questions before submitting your issue. Thanks!

### What version of Go are you using (`go version`)?
go version go1.7.4 linux/386

### What operating system and processor architecture are you using (`go env`)?
GOARCH="386"
GOBIN=""
GOEXE=""
GOHOSTARCH="386"
GOHOSTOS="linux"
GOOS="linux"
GOPATH="/home/robert/workspace.go"
GORACE=""
GOROOT="/usr/lib/go-1.7"
GOTOOLDIR="/usr/lib/go-1.7/pkg/tool/linux_386"
CC="gcc"
GOGCCFLAGS="-fPIC -m32 -pthread -fmessage-length=0 -fdebug-prefix-map=/tmp/go-build941335608=/tmp/go-build -gno-record-gcc-switches"
CXX="g++"
CGO_ENABLED="1"

### What did you do?
If possible, provide a recipe for reproducing the error.
A complete runnable program is good.
A link on play.golang.org is best.

$GOPATH/src/test/reflectCrash/main.go
```
// If the two lines commented BAD are commented out then there is no crash.
package main

import (
        "fmt"
        r "reflect"
        "test/reflectCrash/foo"
        "test/reflectCrash/reflect" // BAD
)

type A struct {
        r reflect.Type // BAD
        f foo.Type
}

func (a A) one() {
}

func (a A) One() string {
        return "Hello"
}

func (a A) Two() (int, bool, string) {
        return 100, false, "Hello"
}

func main() {
        var a A
        fmt.Println("Hello")
        typ := r.TypeOf(a)
        fmt.Printf("num methods %v\n", typ.NumMethod())
        for k := 0; k < typ.NumMethod(); k++ {
                fmt.Printf("method.%v\n", k)
                method := typ.Method(k)
                fmt.Printf("%T %T\n", method, 0)
        }
}
```

$GOPATH/src/test/reflectCrash/reflect/f.go
```
package reflect

import (
        "reflect"
)

type Type reflect.Type
```

$GOPATH/src/test/reflectCrash/foo/f.go
```
package foo

import (
        "reflect"
)

type Type reflect.Type
```


### What did you expect to see?
A program that doesn't crash.

### What did you see instead?
```
Hello
num methods 2
method.0
reflect.Method int
method.1
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0xc pc=0x80a3160]

goroutine 1 [running]:
panic(0x80d4b20, 0x1840a010)
        /usr/lib/go-1.7/src/runtime/panic.go:500 +0x331
reflect.(*rtype).Method(0x80dadc0, 0x1, 0x80c337f, 0x3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, ...)
        /usr/lib/go-1.7/src/reflect/type.go:839 +0x190
main.main()
        /home/robert/workspace.go/src/test/reflectCrash/main.go:33 +0x311
```





I ran this

```
#!/usr/bin/env bash

set -euo pipefail

readonly path=/usr/local/go-git

cd "${path}/src"
GOROOT_BOOTSTRAP=/usr/local/go
GOBIN="${path}/bin"
./make.bash &> /dev/null
cd "${GOBIN}"
mv go /usr/local/bin/go-git
go-git version && go-git run ~/gopath/src/github.com/ericlagergren/issue19028/main.go
```

from HEAD to go1.7beta2.
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `aa1538799601bdbc881f2ad3133184377b7e7aca` and the full history behind it is present.
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
