# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: fatal error: found bad pointer in Go heap (incorrect use of unsafe or cgo?)

<!--
Please answer these questions before submitting your issue. Thanks!
For questions please use one of our forums: https://github.com/golang/go/wiki/Questions
-->

### What version of Go are you using (`go version`)?

<pre>
$ go version
go1.14 linux/amd64
</pre>

### Does this issue reproduce with the latest release?

Yes.

### What operating system and processor architecture are you using (`go env`)?

<details><summary><code>go env</code> Output</summary><br><pre>
$ go env

</pre></details>

### What did you do?

I built a version of my program with a minor code change, and for the first time switching from the go 1.13 compiler to go 1.14. I then deployed that version of the program to my staging environment, all linux/amd64 machines.

### What did you expect to see?

The program to start up normally on all hosts.

### What did you see instead?

On about half of the hosts, the program crashed on startup with slight variations on this message:

<pre>
runtime: pointer 0xc0034fbd40 to unused region of span span.base()=0xc006bf2000 span.limit=0xc006c67300 span.state=1
runtime: found in object at *(0xc000425110+0x28)
object=0xc000425110 s.base()=0xc000424000 s.limit=0xc000425fb0 s.spanclass=28 s.elemsize=208 s.state=mSpanInUse
 *(object+0) = 0x1010100000080
 *(object+8) = 0xc0034fb980
 *(object+16) = 0x8726ce
 *(object+24) = 0x0
 *(object+32) = 0x0
 *(object+40) = 0xc0034fbd40 <==
 *(object+48) = 0xc0a6c8
 *(object+56) = 0xc0034fbaf0
 *(object+64) = 0x872431
 *(object+72) = 0x0
 *(object+80) = 0x0
 *(object+88) = 0x0
 *(object+96) = 0x0
 *(object+104) = 0x0
 *(object+112) = 0x0
 *(object+120) = 0x0
 *(object+128) = 0x0
 *(object+136) = 0x0
 *(object+144) = 0x0
 *(object+152) = 0x0
 *(object+160) = 0x0
 *(object+168) = 0x0
 *(object+176) = 0x0
 *(object+184) = 0x0
 *(object+192) = 0x0
 *(object+200) = 0x0
fatal error: found bad pointer in Go heap (incorrect use of unsafe or cgo?)
runtime stack:
runtime.throw(0xbc9a25, 0x3e)
        /opt/go/src/runtime/panic.go:1112 +0x72 fp=0x7fb9c77fdd30 sp=0x7fb9c77fdd00 pc=0x436132
runtime.badPointer(0x7fba3c4cf108, 0xc0034fbd40, 0xc000425110, 0x28)
        /opt/go/src/runtime/mbitmap.go:380 +0x230 fp=0x7fb9c77fdd78 sp=0x7fb9c77fdd30 pc=0x416410
runtime.findObject(0xc0034fbd40, 0xc000425110, 0x28, 0x7fba3c659d20, 0xc000036e98, 0x7)
        /opt/go/src/runtime/mbitmap.go:416 +0x9b fp=0x7fb9c77fddb0 sp=0x7fb9c77fdd78 pc=0x4164bb
runtime.scanobject(0xc000425110, 0xc000036e98)
        /opt/go/src/runtime/mgcmark.go:1274 +0x235 fp=0x7fb9c77fde40 sp=0x7fb9c77fddb0 pc=0x421555
runtime.gcDrain(0xc000036e98, 0x2)
        /opt/go/src/runtime/mgcmark.go:1032 +0x1fb fp=0x7fb9c77fde98 sp=0x7fb9c77fde40 pc=0x420d5b
runtime.gcBgMarkWorker.func2()
        /opt/go/src/runtime/mgc.go:1951 +0x11e fp=0x7fb9c77fded8 sp=0x7fb9c77fde98 pc=0x46383e
runtime.systemstack(0x7fb9e6ffcb70)
        /opt/go/src/runtime/asm_amd64.s:370 +0x66 fp=0x7fb9c77fdee0 sp=0x7fb9c77fded8 pc=0x466976
runtime.mstart()
        /opt/go/src/runtime/proc.go:1041 fp=0x7fb9c77fdee8 sp=0x7fb9c77fdee0 pc=0x43af10
</pre>

I don't use unsafe or cgo in my program directly, though some of my transitive dependencies might, I can't say for sure.

Small update: just confirmed that this issue persists with 1.14.1.
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `585e31df63f6879c03b285711de6f9dcba1f2cb0` and the full history behind it is present.
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
