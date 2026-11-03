# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/compile: inefficient code generation on amd64

### Probably, inefficient code generation on amd64.



#### Preface

Examining the assembly code listing, I found out that the compiler generates sub-optimal code for some part of the code.
I will not describe the whole journey. I found a code (code from benchmark game) illustrating the problem and will use it for an example.

All source code: https://benchmarksgame-team.pages.debian.net/benchmarksgame/program/nbody-go-3.html

Let's pay attention to these lines (60, 61, 62), it's "advance" func:

```go
dx := sys.s[i].x - sys.s[j].x
dy := sys.s[i].y - sys.s[j].y
dz := sys.s[i].z - sys.s[j].z
```

Let's take a look at the result of the code generation:

```
  main.go:60    LEAQ 0(CX)(CX*2), DI         // DI = i, BX = j
  main.go:60    LEAQ main.sys+160(SB), R8

  main.go:60    MOVSD_XMM 0(R8)(DI*8), X4    // load x +0x0
  main.go:60    LEAQ 0(BX)(BX*2), R9         // calculate offset for .x
  main.go:60    LEAQ 0(R8)(R9*8), R10        // sys.s[j] + offset
  main.go:60    SUBSD 0(R10), X4

  main.go:61    MOVSD_XMM 0x8(R8)(DI*8), X5  // load y +0x8
  main.go:61    LEAQ 0(R8)(R9*8), R10
  main.go:61    LEAQ 0x8(R10), R10
  main.go:61    SUBSD 0(R10), X5

  main.go:62    MOVSD_XMM 0x10(R8)(DI*8), X6 // load z +0x10
  main.go:62    LEAQ 0(R8)(R9*8), DI
  main.go:62    LEAQ 0x10(DI), DI
  main.go:62    SUBSD 0(DI), X6
```

We need one instruction to load the value of the left operand and two to calculate the address of the right one.

I rolled back to version go1.14 and found that the codegen there is different. For the same lines, the following code will be generated:

```
  main.go:60    0x49f77d    LEAQ 0(CX)(CX*2), DI              // DI = 0
  main.go:60    0x49f781    LEAQ main.sys+160(SB), R8         // R8 = Positions addr

  main.go:60    0x49f788    MOVSD_XMM 0(R8)(DI*8), X4         // load sys.s[i].x
  main.go:60    0x49f78e    LEAQ 0(BX)(BX*2), R9
  main.go:60    0x49f792    MOVSD_XMM 0(R8)(R9*8), X5         // load sys.s[j].x
  main.go:60    0x49f798    SUBSD X5, X4

  main.go:61    0x49f79c    MOVSD_XMM 0x8(R8)(DI*8), X5
  main.go:61    0x49f7a3    MOVSD_XMM 0x8(R8)(R9*8), X6       // dy := sys.s[i].y - sys.s[j].y
  main.go:61    0x49f7aa    SUBSD X6, X5

  main.go:62    0x49f7ae    MOVSD_XMM 0x10(R8)(DI*8), X6
  main.go:62    0x49f7b5    MOVSD_XMM 0x10(R8)(R9*8), X7      // dz := sys.s[i].z - sys.s[j].z
  main.go:62    0x49f7bc    SUBSD X7, X6
```

It uses one instruction to load both the left and right side of the expression.

#### How does it affect code performance?

It depends on how often such a code generation pattern is used in the code and in how hot the pieces of code are.
But we can write benchmark:

```go
package main

import (
    "testing"
)

func BenchmarkT(b *testing.B) {
    offsetMomentum()
    c := 500000

    b.ResetTimer()
    for n := 0; n < b.N; n++ {
        for i := 0; i < c; i++ {
            advance(0.01)
        }
    }

    _ = energy()
}
```

Results:

```
$ bin for i in {1..20}; do go.1.14 test -bench=. >> old.txt; done
$ bin for i in {1..20}; do go.master test -bench=. >> new.txt; done
$ bin benchstat old.txt new.txt
name  old time/op  new time/op  delta
T-4   48.9ms ± 5%  54.5ms ±10%  +11.46%  (p=0.000 n=19+19)
```

#### When did the issue start?







/cc @randall77
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `8696ae82c94f0a7707cbbbdf2cec44e93edf5b23` and the full history behind it is present.
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
