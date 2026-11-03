# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: Go 1.17, Windows unexpected return pc for runtime.call16 called



```
runtime: unknown pc 0x8bf33ff3a0
stack: frame={sp:0xc00009f6d0, fp:0x0} stack=[0xc00009c000,0xc0000a0000)
0x000000c00009f5d0:  0x000000c00009f6a0  0x0000000000b182a5 
...

// or

runtime: unexpected return pc for runtime.call16 called from 0x31bc7ff340
stack: frame={sp:0xc00019f6a8, fp:0xc00019f6c8} stack=[0xc00019c000,0xc0001a0000)
0x000000c00019f5a8:  0x0101016c7d38df00  0x00013e459581e920
0x000000c00019f5b8:  0x0000000000000000  0x000000c00019f5f0
...
```

Easiest way to reproduce the issue is:
```
go install gioui.org/example/hello@latest && hello
```

<details><summary><code>hello</code> crash output</summary>

```
Exception 0xc0000005 0x8 0x8bf33ff3a0 0x8bf33ff3a0
PC=0x8bf33ff3a0

runtime: unknown pc 0x8bf33ff3a0
stack: frame={sp:0xc00009f6d0, fp:0x0} stack=[0xc00009c000,0xc0000a0000)
0x000000c00009f5d0:  0x000000c00009f6a0  0x0000000000b182a5 <gioui.org/app/internal/wm.windowProc+0x0000000000000a25>
0x000000c00009f5e0:  0x000000c0000c7e60  0x000000c00011e040
0x000000c00009f5f0:  0x0000000000000004  0x0000000000000004
0x000000c00009f600:  0x0065006c00690066  0x0000000000000066
0x000000c00009f610:  0x0000000000a2262c <runtime.reflectcallmove+0x000000000000006c>  0x000000000000000f
0x000000c00009f620:  0x000000c00009f668  0x0000000000cb07fc
0x000000c00009f630:  0x000000c00009f668  0x0000000000a72c85 <runtime.reflectcallmove+0x0000000000000045>
0x000000c00009f640:  0x0074006300650073  0x0000000000000000
0x000000c00009f650:  0x0000000000000000  0x000001f93e040778
0x000000c00009f660:  0x000000c00009f988  0x000000c00009f6a0
0x000000c00009f670:  0x0000000000a6da8b <callRet+0x000000000000002b>  0x0000000000000000
0x000000c00009f680:  0x000000c00009f738  0x000000c00009f6b0
0x000000c00009f690:  0x0000000000000000  0x000000c00009f988
0x000000c00009f6a0:  0x000000c00009f6c0  0x0000000000a6edfd <runtime.call16+0x000000000000007d>
0x000000c00009f6b0:  0x0000000000cb07fc  0x000001f900000024
0x000000c00009f6c0:  0x0000000000000000  0x0000008bf33ff3a0
0x000000c00009f6d0: <0x0000000000000000  0x0000000000bc2d20
0x000000c00009f6e0:  0x000000c00009f738  0x0000000000000000
0x000000c00009f6f0:  0x000000c000000000  0x000000c00009f988
0x000000c00009f700:  0x0000000000000003  0x0000000000000004
0x000000c00009f710:  0x0000000000000002  0x0000000000000018
0x000000c00009f720:  0x0000000000000000  0x0000000000000003
0x000000c00009f730:  0x0000000000000008  0x0000000000000000
0x000000c00009f740:  0x0000000000000000  0x0000000000000000
0x000000c00009f750:  0x0000000000000000  0x0000000000000000
0x000000c00009f760:  0x0000000000000000  0x0000000000000000
0x000000c00009f770:  0x0000000000000000  0x0000000000000000
0x000000c00009f780:  0x0000000000000000  0x0000000000000000
0x000000c00009f790:  0x0000000000000000  0x0000000000000000
0x000000c00009f7a0:  0x0000000000000000  0x0000000000000000
0x000000c00009f7b0:  0x0000000000000000  0x0000000000000000
0x000000c00009f7c0:  0x0000000000000000  0x0000000000000000
runtime: unknown pc 0x8bf33ff3a0
stack: frame={sp:0xc00009f6d0, fp:0x0} stack=[0xc00009c000,0xc0000a0000)
0x000000c00009f5d0:  0x000000c00009f6a0  0x0000000000b182a5 <gioui.org/app/internal/wm.windowProc+0x0000000000000a25>
0x000000c00009f5e0:  0x000000c0000c7e60  0x000000c00011e040
0x000000c00009f5f0:  0x0000000000000004  0x0000000000000004
0x000000c00009f600:  0x0065006c00690066  0x0000000000000066
0x000000c00009f610:  0x0000000000a2262c <runtime.reflectcallmove+0x000000000000006c>  0x000000000000000f
0x000000c00009f620:  0x000000c00009f668  0x0000000000cb07fc
0x000000c00009f630:  0x000000c00009f668  0x0000000000a72c85 <runtime.reflectcallmove+0x0000000000000045>
0x000000c00009f640:  0x0074006300650073  0x0000000000000000
0x000000c00009f650:  0x0000000000000000  0x000001f93e040778
0x000000c00009f660:  0x000000c00009f988  0x000000c00009f6a0
0x000000c00009f670:  0x0000000000a6da8b <callRet+0x000000000000002b>  0x0000000000000000
0x000000c00009f680:  0x000000c00009f738  0x000000c00009f6b0
0x000000c00009f690:  0x0000000000000000  0x000000c00009f988
0x000000c00009f6a0:  0x000000c00009f6c0  0x0000000000a6edfd <runtime.call16+0x000000000000007d>
0x000000c00009f6b0:  0x0000000000cb07fc  0x000001f900000024
0x000000c00009f6c0:  0x0000000000000000  0x0000008bf33ff3a0
0x000000c00009f6d0: <0x0000000000000000  0x0000000000bc2d20
0x000000c00009f6e0:  0x000000c00009f738  0x0000000000000000
0x000000c00009f6f0:  0x000000c000000000  0x000000c00009f988
0x000000c00009f700:  0x0000000000000003  0x0000000000000004
0x000000c00009f710:  0x0000000000000002  0x0000000000000018
0x000000c00009f720:  0x0000000000000000  0x0000000000000003
0x000000c00009f730:  0x0000000000000008  0x0000000000000000
0x000000c00009f740:  0x0000000000000000  0x0000000000000000
0x000000c00009f750:  0x0000000000000000  0x0000000000000000
0x000000c00009f760:  0x0000000000000000  0x0000000000000000
0x000000c00009f770:  0x0000000000000000  0x0000000000000000
0x000000c00009f780:  0x0000000000000000  0x0000000000000000
0x000000c00009f790:  0x0000000000000000  0x0000000000000000
0x000000c00009f7a0:  0x0000000000000000  0x0000000000000000
0x000000c00009f7b0:  0x0000000000000000  0x0000000000000000
0x000000c00009f7c0:  0x0000000000000000  0x0000000000000000
created by gioui.org/app/internal/wm.NewWindow
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/internal/wm/os_windows.go:101 +0xc8

goroutine 1 [select (no cases)]:
gioui.org/app/internal/wm.Main()
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/internal/wm/os_windows.go:96 +0x17
gioui.org/app.Main(...)
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/app.go:53
main.main()
        F:/Go/pkg/mod/gioui.org/example@v0.0.0-20210520083412-9861f99f710d/hello/hello.go:30 +0x2b

goroutine 6 [chan receive]:
main.loop(0xc000008480)
        F:/Go/pkg/mod/gioui.org/example@v0.0.0-20210520083412-9861f99f710d/hello/hello.go:37 +0x79
main.main.func1()
        F:/Go/pkg/mod/gioui.org/example@v0.0.0-20210520083412-9861f99f710d/hello/hello.go:25 +0x2a
created by main.main
        F:/Go/pkg/mod/gioui.org/example@v0.0.0-20210520083412-9861f99f710d/hello/hello.go:23 +0x25

goroutine 7 [chan receive]:
gioui.org/app/internal/wm.NewWindow({0xbf5110, 0xc000008878}, 0xc0000900a0)
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/internal/wm/os_windows.go:129 +0xdd
gioui.org/app.(*Window).run(0xc000008480, 0x0)
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/window.go:432 +0xca
created by gioui.org/app.NewWindow
        F:/Go/pkg/mod/gioui.org@v0.0.0-20210519204653-f8d201b7c23d/app/window.go:117 +0x35e
rax     0x9
rbx     0x0
rcx     0x0
rdi     0xc00009f738
rsi     0x8
rbp     0x0
rsp     0xc00009f6d0
r8      0xffffffff
r9      0x1
r10     0xcb07fc
r11     0x30000
r12     0xc00009f988
r13     0x0
r14     0xc0001041a0
r15     0x6
rip     0x8bf33ff3a0
rflags  0x10202
cs      0x33
fs      0x53
gs      0x2b
```

</details>

The issue also happens with https://play.golang.org/p/2JzHDalGN7Q from https://github.com/golang/go/issues/34474.

<details><summary><code>playground</code> crash output</summary>

```
runtime: unexpected return pc for runtime.call16 called from 0x31bc7ff340
stack: frame={sp:0xc00019f6a8, fp:0xc00019f6c8} stack=[0xc00019c000,0xc0001a0000)
0x000000c00019f5a8:  0x0101016c7d38df00  0x00013e459581e920
0x000000c00019f5b8:  0x0000000000000000  0x000000c00019f5f0
0x000000c00019f5c8:  0x000000000013739b <runtime.gcWaitOnMark+0x000000000000005b>  0x0000000000000000
0x000000c00019f5d8:  0x0000000000275b20  0x0000000000137ac0 <runtime.gcStart.func2+0x0000000000000000>
0x000000c00019f5e8:  0x000000c0001c95b0  0x000000c00019f628
0x000000c00019f5f8:  0x000000000013722e <runtime.GC+0x000000000000004e>  0x0000000000000001
0x000000c00019f608:  0x0000000000000000  0x0000000000000000
0x000000c00019f618:  0x0000000100000000  0x0000000000000000
0x000000c00019f628:  0x000000c00019f698  0x00000000001b7096 <main.windowProc+0x0000000000000036>
0x000000c00019f638:  0x0000000000000000  0x0000000000000000
0x000000c00019f648:  0x0000000000000000  0x0000000000000000
0x000000c00019f658:  0x0000000000000000  0x0000000000000000
0x000000c00019f668:  0x0000000000000000  0x0000000000000000
0x000000c00019f678:  0x0000000000000000  0x0000000000000000
0x000000c00019f688:  0x0000000000000000  0x0000000000000000
0x000000c00019f698:  0x000000c00019f6b8  0x000000000017bc30 <runtime.call16+0x0000000000000050>
0x000000c00019f6a8: <0x0000000000160b70 <runtime.sysmon+0x0000000000000390>  0x0000000000000024
0x000000c00019f6b8:  0x0000000000000000 !0x00000031bc7ff340
0x000000c00019f6c8: >0x0000000000000000  0x00000000001dadf0
0x000000c00019f6d8:  0x000000c0001c9730  0x0000000000000000
0x000000c00019f6e8:  0x0000000000000000  0x000000c0001c9980
0x000000c00019f6f8:  0x0000000000000003  0x0000000000000004
0x000000c00019f708:  0x0000000000000002  0x0000000000000018
0x000000c00019f718:  0x0000000000000000  0x0000000000000003
0x000000c00019f728:  0x0000000000000008  0x0000000000000000
0x000000c00019f738:  0x0000000000000000  0x0000000000000000
0x000000c00019f748:  0x0000000000000000  0x0000000000000000
0x000000c00019f758:  0x0000000000000000  0x0000000000000000
0x000000c00019f768:  0x0000000000000000  0x0000000000000000
0x000000c00019f778:  0x0000000000000000  0x0000000000000000
0x000000c00019f788:  0x0000000000000000  0x0000000000000000
0x000000c00019f798:  0x0000000000000000  0x0000000000000000
0x000000c00019f7a8:  0x0000000000000000  0x0000000000000000
0x000000c00019f7b8:  0x0000000000000000  0x0000000000000000
fatal error: unknown caller pc

runtime stack:
runtime.throw({0x1d3ad9, 0x262a40})
        C:/Go.tip/src/runtime/panic.go:1198 +0x76
runtime.gentraceback(0x31bcfff448, 0x135b0e, 0x7fff30208500, 0xc000104000, 0x0, 0x0, 0x7fffffff, 0x1dae10, 0x31bcfff460, 0x0)
        C:/Go.tip/src/runtime/traceback.go:278 +0x1956
runtime.copystack(0xc000074000, 0x4000)
        C:/Go.tip/src/runtime/stack.go:918 +0x293
runtime.shrinkstack(0xc000074000)
        C:/Go.tip/src/runtime/stack.go:1197 +0x126
runtime.scanstack(0xc000074000, 0xc00002a698)
        C:/Go.tip/src/runtime/mgcmark.go:719 +0xb2
runtime.markroot.func1()
        C:/Go.tip/src/runtime/mgcmark.go:232 +0xb1
runtime.markroot(0xc00002a698, 0x6)
        C:/Go.tip/src/runtime/mgcmark.go:205 +0x170
runtime.gcDrain(0xc00002a698, 0x7)
        C:/Go.tip/src/runtime/mgcmark.go:1013 +0x379
runtime.gcBgMarkWorker.func2()
        C:/Go.tip/src/runtime/mgc.go:1288 +0x6e
runtime.systemstack()
        C:/Go.tip/src/runtime/asm_amd64.s:383 +0x4e

goroutine 26 [GC worker (idle)]:
runtime.systemstack_switch()
        C:/Go.tip/src/runtime/asm_amd64.s:350 fp=0xc0001e7f60 sp=0xc0001e7f58 pc=0x17b6e0
runtime.gcBgMarkWorker()
        C:/Go.tip/src/runtime/mgc.go:1256 +0x1b8 fp=0xc0001e7fe0 sp=0xc0001e7f60 pc=0x138f58
runtime.goexit()
        C:/Go.tip/src/runtime/asm_amd64.s:1581 +0x1 fp=0xc0001e7fe8 sp=0xc0001e7fe0 pc=0x17da61
created by runtime.gcBgMarkStartWorkers
        C:/Go.tip/src/runtime/mgc.go:1124 +0x25

goroutine 1 [wait for GC cycle (scan), locked to thread]:
runtime.GC()
        C:/Go.tip/src/runtime/mgc.go:441 +0x4e
main.windowProc(0x160b70, 0x24, 0x0, 0x31bc7ff340)
        f:/Code/sandbox/demo/main.go:148 +0x36
fatal error: unexpected signal during runtime execution
panic during panic
[signal 0xc0000005 code=0x0 addr=0xe8 pc=0x1715dc]

runtime stack:
runtime.throw({0x1d927b, 0x1})
        C:/Go.tip/src/runtime/panic.go:1198 +0x76
runtime.sigpanic()
        C:/Go.tip/src/runtime/signal_windows.go:237 +0x22b
runtime.gentraceback(0x0, 0xc00007e800, 0x31bcffed10, 0x150425, 0x0, 0x0, 0x64, 0x0, 0x0, 0x0)
        C:/Go.tip/src/runtime/traceback.go:266 +0x73c
runtime.traceback1(0xc000074000, 0x155300, 0x0, 0xc000074000, 0x1742cf)
        C:/Go.tip/src/runtime/traceback.go:827 +0x173
runtime.traceback(...)
        C:/Go.tip/src/runtime/traceback.go:781
runtime.tracebackothers.func1(0xc000074000)
        C:/Go.tip/src/runtime/traceback.go:1043 +0xe5
runtime.forEachGRace(0x31bcffef48)
        C:/Go.tip/src/runtime/proc.go:593 +0x4d
runtime.tracebackothers(0xc000074820)
        C:/Go.tip/src/runtime/traceback.go:1029 +0xdb
runtime.dopanic_m(0xc000074820, 0x153b76, 0x31bcfff048)
        C:/Go.tip/src/runtime/panic.go:1398 +0x21c
runtime.fatalthrow.func1()
        C:/Go.tip/src/runtime/panic.go:1253 +0x48
runtime.fatalthrow()
        C:/Go.tip/src/runtime/panic.go:1250 +0x50
runtime.throw({0x1d3ad9, 0x262a40})
        C:/Go.tip/src/runtime/panic.go:1198 +0x76
runtime.gentraceback(0x31bcfff448, 0x135b0e, 0x7fff30208500, 0xc000104000, 0x0, 0x0, 0x7fffffff, 0x1dae10, 0x31bcfff460, 0x0)
        C:/Go.tip/src/runtime/traceback.go:278 +0x1956
runtime.copystack(0xc000074000, 0x4000)
        C:/Go.tip/src/runtime/stack.go:918 +0x293
runtime.shrinkstack(0xc000074000)
        C:/Go.tip/src/runtime/stack.go:1197 +0x126
runtime.scanstack(0xc000074000, 0xc00002a698)
        C:/Go.tip/src/runtime/mgcmark.go:719 +0xb2
runtime.markroot.func1()
        C:/Go.tip/src/runtime/mgcmark.go:232 +0xb1
runtime.markroot(0xc00002a698, 0x6)
        C:/Go.tip/src/runtime/mgcmark.go:205 +0x170
runtime.gcDrain(0xc00002a698, 0x7)
        C:/Go.tip/src/runtime/mgcmark.go:1013 +0x379
runtime.gcBgMarkWorker.func2()
        C:/Go.tip/src/runtime/mgc.go:1288 +0x6e
runtime.systemstack()
        C:/Go.tip/src/runtime/asm_amd64.s:383 +0x4e
exit status 2
```

</details>
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `831573cd21e65c37b4e1bf5d44dc23b125084b7a` and the full history behind it is present.
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
