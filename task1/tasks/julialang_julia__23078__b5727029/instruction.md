# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Exception access violation

0.7 crashes on all architectures.
In the file FEMMBaseModule.jl, the call of the function on line 327 triggers the collapse:
```
  idat = inspectintegpoints(self,  geom,  u,  dT,
            collect(1:count(geod.fes)),  idi_inspector,  idat, quantity;
            context...);
```
This very same code runs fine with 0.6.

The issue can be reproduced by running test_failing.jl, or
```
Pkg.clone("https://github.com/PetrKryslUCSD/FinEtools.jl")
using FinEtools
Pkg.test("FinEtools")
```
Here is the  detailed message  in the terminal window (Windows 10 64-bit).




Also reproducible on linux x86_64 (didn't check if bisect would point to the same thing there yet), where some of the time it gives an LLVM assertion failure instead of a segfault, if you've built with `override LLVM_ASSERTIONS = 1` in your `Make.user`. The assertion failure doesn't look like it's always the same, but one case was
```
julia: /home/tkelman/Julia/julia-0.7/deps/srccache/llvm-3.9.1/include/llvm/Support/Casting.h:237: typename llvm::cast_retty<X, Y*>::ret_type llvm::cast(Y*) [with X = llvm::PointerType; Y = llvm::Type; typename llvm::cast_retty<X, Y*>::ret_type = llvm::PointerType*]: Assertion `isa<X>(Val) && "cast<Ty>() argument of incompatible type!"' failed.

signal (6): Aborted
while loading /home/tkelman/.julia/v0.7/FinEtools/test/test_failing.jl, in expression starting on line 77
raise at /build/eglibc-SvCtMH/eglibc-2.19/signal/../nptl/sysdeps/unix/sysv/linux/raise.c:56
abort at /build/eglibc-SvCtMH/eglibc-2.19/stdlib/abort.c:89
__assert_fail_base at /build/eglibc-SvCtMH/eglibc-2.19/assert/assert.c:92
__assert_fail at /build/eglibc-SvCtMH/eglibc-2.19/assert/assert.c:101
_ZN4llvm4castINS_11PointerTypeENS_4TypeEEENS_10cast_rettyIT_PT0_E8ret_typeES6_.part.248 at /home/tkelman/Julia/julia-0.7/usr/bin/../lib/libLLVM-3.9.so (unknown line)
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `fb76529050cdf142ce6614b28d690fff560e8d3a` and the full history behind it is present.
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
