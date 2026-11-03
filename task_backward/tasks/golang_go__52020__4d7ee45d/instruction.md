# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/compile: internal compiler error: unhandled OCONV ARRAY -> UINT8

Compiler failure with tip:

<pre>
$ go version

</pre>

```
package main

func main() {
        var _ interface{} = struct{ _ [1]int8 }{}
}
```

```
$ go run .
./main.go:4:41: internal compiler error: 'main': unhandled OCONV ARRAY -> UINT8

goroutine 49 [running]:
runtime/debug.Stack()
        /usr/local/google/home/dneil/src/go/src/runtime/debug/stack.go:24 +0x65
cmd/compile/internal/base.FatalfAt({0xc7ca60?, 0x0?}, {0xc00042b8d0, 0x1e}, {0xc0007142d0, 0x3, 0x3})
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/base/print.go:227 +0x1d7
cmd/compile/internal/base.Fatalf(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/base/print.go:196
cmd/compile/internal/ssagen.(*ssafn).Fatalf(0x0?, {0x0?, 0x0?}, {0xd0b605, 0x18}, {0xc00070c140, 0x2, 0x0?})
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:7676 +0x17d
cmd/compile/internal/ssagen.(*state).Fatalf(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:925
cmd/compile/internal/ssagen.(*state).conv(0xc0005c4100, {0xe63290, 0xc0007101e0}, 0x1?, 0xc0003e8bd0, 0xc00037e230)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2526 +0x1f49
cmd/compile/internal/ssagen.(*state).exprCheckPtr(0xc0005c4100, {0xe63290?, 0xc0007101e0?}, 0x1)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2724 +0x1cda
cmd/compile/internal/ssagen.(*state).expr(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2532
cmd/compile/internal/ssagen.(*state).exprCheckPtr(0xc0005c4100, {0xe63290?, 0xc000710230?}, 0x1)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2723 +0x1c8b
cmd/compile/internal/ssagen.(*state).expr(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2532
cmd/compile/internal/ssagen.(*state).exprCheckPtr(0xc0005c4100, {0xe62c18?, 0xc000726060?}, 0x1)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2892 +0x49eb
cmd/compile/internal/ssagen.(*state).expr(0xc0005c4100?, {0xe62c18?, 0xc000726060?})
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2532 +0x28
cmd/compile/internal/ssagen.(*state).addr(0xc0005c4100, {0xe639c0, 0xc0007260c0})
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:5233 +0xbdf
cmd/compile/internal/ssagen.(*state).exprCheckPtr(0xc0005c4100, {0xe62880?, 0xc000710320?}, 0x1)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2978 +0x154a
cmd/compile/internal/ssagen.(*state).expr(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2532
cmd/compile/internal/ssagen.(*state).exprCheckPtr(0xc0005c4100, {0xe62c18?, 0xc000726180?}, 0x1)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:3114 +0x693e
cmd/compile/internal/ssagen.(*state).expr(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:2532
cmd/compile/internal/ssagen.(*state).stmt(0xc0005c4100, {0xe62aa8, 0xc0003e6dc0?})
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:1581 +0xade
cmd/compile/internal/ssagen.(*state).stmtList(...)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:1371
cmd/compile/internal/ssagen.buildssa(0xc000405cc0, 0x0)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/ssa.go:554 +0x1ea9
cmd/compile/internal/ssagen.Compile(0xc000405cc0, 0xc0005bc790?)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/ssagen/pgen.go:183 +0x4c
cmd/compile/internal/gc.compileFunctions.func4.1(0x0?)
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/gc/compile.go:153 +0x3a
cmd/compile/internal/gc.compileFunctions.func3.1()
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/gc/compile.go:140 +0x4d
created by cmd/compile/internal/gc.compileFunctions.func3
        /usr/local/google/home/dneil/src/go/src/cmd/compile/internal/gc/compile.go:138 +0x78
```


My bisect blames:





cc @cuonglm @randall77
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `a4a0f9b1481e9be4361eb9c4998eca08e2eedb0a` and the full history behind it is present.
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
