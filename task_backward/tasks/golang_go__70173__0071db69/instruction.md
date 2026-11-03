# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: unexpected return pc from label followed by fallthrough

### Go version

Go 1.23

### Output of `go env` in your module/workspace:

```shell
/
```


### What did you do?

Playground: https://go.dev/play/p/Cb94cJlyvNM
```go
package main

func main() {
	switch {
	case true:
		goto a
	a:
		fallthrough
	default:
	}
}
```

### What did you see happen?

SIGTRAP: trace trap
PC=0x466522 m=0 sigcode=128

goroutine 1 gp=0xc0000061c0 m=0 mp=0x4ef280 [running]:
main.main()
	?:0 +0x2 fp=0xc00004874f sp=0xc000048748 pc=0x466522
runtime: g 1: unexpected return pc for main.main called from 0x43116b00
stack: frame={sp:0xc000048748, fp:0xc00004874f} stack=[0xc000048000,0xc000048800)
0x000000c000048648:  0x000000c000048660  0x00000000004122f6 <runtime.gcTrigger.test+0x00000000000000b6> 
0x000000c000048658:  0x000000000050e920  0x000000c000048700 
0x000000c000048668:  0x000000000045b6a5 <runtime.mallocgc+0x0000000000000925>  0x00007ec01177d5b8 
0x000000c000048678:  0x000000c000048613  0x0000000000405888 <runtime.chanrecv+0x00000000000004e8> 
0x000000c000048688:  0x000000c00009e000  0x00007ebfcac815e8 
0x000000c000048698:  0x0000010100000010  0x00007ebfcac81368 
0x000000c0000486a8:  0x0000000000000070  0x0100000000000010 
0x000000c0000486b8:  0x00007ec01177d5b8  0x000000c0000486e8 
0x000000c0000486c8:  0x0000000000409db0 <runtime.unlock2+0x0000000000000050>  0x000000c000098060 
0x000000c0000486d8:  0x00000000004ef280  0x000000c0000061c0 
0x000000c0000486e8:  0x000000c000048740  0x00000000004051eb <runtime.closechan+0x000000000000034b> 
0x000000c0000486f8:  0x0000000000405392 <runtime.chanrecv1+0x0000000000000012>  0x000000c000048740 
0x000000c000048708:  0x0000000000000000  0x0000000000000068 
0x000000c000048718:  0x0000000000000000  0x000000c0000a2060 
0x000000c000048728:  0x00000000004ea378  0x000000000046c5c0 
0x000000c000048738:  0x000000c0000061c0  0x000000c0000487d0 
0x000000c000048748: <0x000000000043116b <runtime.main+0x000000000000028b>  0x000000c0000a2000 
0x000000c000048758:  0x0000000000000000  0x0000000000000000 
0x000000c000048768:  0x0000000000000000  0x0100000000000000 
0x000000c000048778:  0x0000000000000000  0x0000000000000002 
0x000000c000048788:  0x00000000004ea860  0x0000000000000000 
0x000000c000048798:  0x0000000000000001  0x00000000004ea100 
0x000000c0000487a8:  0x00000000004ea1c0  0x00000000004ef280 
0x000000c0000487b8:  0x0000000000431300 <runtime.main.func2+0x0000000000000000>  0x000000c000048776 
0x000000c0000487c8:  0x000000c0000487b8  0x0000000000000000 
0x000000c0000487d8:  0x00000000004634c1 <runtime.goexit+0x0000000000000001>  0x0000000000000000 
0x000000c0000487e8:  0x0000000000000000  0x0000000000000000 
0x000000c0000487f8:  0x0000000000000000 

goroutine 2 gp=0xc000006700 m=nil [force gc (idle)]:
runtime.gopark(0x0?, 0x0?, 0x0?, 0x0?, 0x0?)
	/usr/local/go-faketime/src/runtime/proc.go:424 +0xce fp=0xc000048fa8 sp=0xc000048f88 pc=0x45d2ee
runtime.goparkunlock(...)
	/usr/local/go-faketime/src/runtime/proc.go:430
runtime.forcegchelper()
	/usr/local/go-faketime/src/runtime/proc.go:337 +0xa5 fp=0xc000048fe0 sp=0xc000048fa8 pc=0x4314a5
runtime.goexit({})
	/usr/local/go-faketime/src/runtime/asm_amd64.s:1700 +0x1 fp=0xc000048fe8 sp=0xc000048fe0 pc=0x4634c1
created by runtime.init.7 in goroutine 1
	/usr/local/go-faketime/src/runtime/proc.go:325 +0x1a

goroutine 17 gp=0xc000084380 m=nil [GC sweep wait]:
runtime.gopark(0x0?, 0x0?, 0x0?, 0x0?, 0x0?)
	/usr/local/go-faketime/src/runtime/proc.go:424 +0xce fp=0xc000044780 sp=0xc000044760 pc=0x45d2ee
runtime.goparkunlock(...)
	/usr/local/go-faketime/src/runtime/proc.go:430
runtime.bgsweep(0xc000098000)
	/usr/local/go-faketime/src/runtime/mgcsweep.go:277 +0x94 fp=0xc0000447c8 sp=0xc000044780 pc=0x41d6b4
runtime.gcenable.gowrap1()
	/usr/local/go-faketime/src/runtime/mgc.go:203 +0x25 fp=0xc0000447e0 sp=0xc0000447c8 pc=0x412185
runtime.goexit({})
	/usr/local/go-faketime/src/runtime/asm_amd64.s:1700 +0x1 fp=0xc0000447e8 sp=0xc0000447e0 pc=0x4634c1
created by runtime.gcenable in goroutine 1
	/usr/local/go-faketime/src/runtime/mgc.go:203 +0x66

goroutine 18 gp=0xc000084540 m=nil [GC scavenge wait]:
runtime.gopark(0xc000098000?, 0x4948b8?, 0x1?, 0x0?, 0xc000084540?)
	/usr/local/go-faketime/src/runtime/proc.go:424 +0xce fp=0xc000044f78 sp=0xc000044f58 pc=0x45d2ee
runtime.goparkunlock(...)
	/usr/local/go-faketime/src/runtime/proc.go:430
runtime.(*scavengerState).park(0x4ee4e0)
	/usr/local/go-faketime/src/runtime/mgcscavenge.go:425 +0x49 fp=0xc000044fa8 sp=0xc000044f78 pc=0x41b129
runtime.bgscavenge(0xc000098000)
	/usr/local/go-faketime/src/runtime/mgcscavenge.go:653 +0x3c fp=0xc000044fc8 sp=0xc000044fa8 pc=0x41b65c
runtime.gcenable.gowrap2()
	/usr/local/go-faketime/src/runtime/mgc.go:204 +0x25 fp=0xc000044fe0 sp=0xc000044fc8 pc=0x412125
runtime.goexit({})
	/usr/local/go-faketime/src/runtime/asm_amd64.s:1700 +0x1 fp=0xc000044fe8 sp=0xc000044fe0 pc=0x4634c1
created by runtime.gcenable in goroutine 1
	/usr/local/go-faketime/src/runtime/mgc.go:204 +0xa5

rax    0x466520
rbx    0xc0000a2060
rcx    0xc0000061c0
rdx    0x47ee78
rdi    0x1
rsi    0x3d0000
rbp    0xc0000487d0
rsp    0xc000048748
r8     0x0
r9     0x1
r10    0x7ebfcac81368
r11    0x0
r12    0xc0000a2000
r13    0x0
r14    0xc0000061c0
r15    0x0
rip    0x466522
rflags 0x246
cs     0x33
fs     0x0
gs     0x0

### What did you expect to see?

To work without errors.
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `989eed28497cde7145958985f50bb3dd6ab698b6` and the full history behind it is present.
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
