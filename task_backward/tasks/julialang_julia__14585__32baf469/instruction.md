# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Segfault generating inference0.ji with ORC on ARMv7

I'm building latest Julia on ARMv7 with the following `Make.user` (from the ARM README):

```
override USE_SYSTEM_BLAS=1
override USE_SYSTEM_LAPACK=1
override USE_SYSTEM_LIBM=1
override USE_SYSTEM_FFTW=1
override USE_SYSTEM_GMP=1
override USE_SYSTEM_MPFR=1
override USE_SYSTEM_ARPACK=1

override USE_LLVM_SHLIB=1
override LLVM_DEBUG=1
override LLVM_ASSERTIONS=1

override JULIA_BUILD_MODE=debug
```

Debug builds added for the sake of a readable backtrace, but the segfault also happens on non-debug Julia/LLVM.

When building Julia, very early during sysimg generation (more specifically when generating `usr/lib/julia/inference0.ji`) I get a segfault:

```
 ~/julia/base$ ../usr/bin/julia-debug -C native --output-ji ../usr/lib/julia/inference0.ji -f coreimg.jl
zsh: segmentation fault  ../usr/bin/julia-debug -C native --output-ji ../usr/lib/julia/inference0.ji -
```

Attaching GDB, I get a SIGABRT instead... So it might be a different issue, but at least there's a backtrace + assertion failure:

```
Starting program: /home/tbesard/julia/usr/bin/julia-debug -C native --output-ji ../usr/lib/julia/inference0.ji -f coreimg.jl
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/arm-linux-gnueabihf/libthread_db.so.1".
[New Thread 0x74777450 (LWP 15551)]
julia-debug: /home/tbesard/julia/deps/srccache/llvm-3.7.0/include/llvm/Support/Casting.h:269: typename llvm::cast_retty<X, Y*>::ret_type llvm::cast_or_null(Y*) [with X = llvm::MCSymbolELF; Y = llvm::MCSymbol; typename llvm::cast_retty<X, Y*>::ret_type = llvm::MCSymbolELF*]: Assertion `isa<X>(Val) && "cast_or_null<Ty>() argument of incompatible type!"' failed.

Program received signal SIGABRT, Aborted.
__libc_do_syscall () at ../ports/sysdeps/unix/sysv/linux/arm/libc-do-syscall.S:44
44      ../ports/sysdeps/unix/sysv/linux/arm/libc-do-syscall.S: No such file or directory.
(gdb) bt
#0  __libc_do_syscall () at ../ports/sysdeps/unix/sysv/linux/arm/libc-do-syscall.S:44
#1  0x76c270fe in __GI_raise (sig=sig@entry=6) at ../nptl/sysdeps/unix/sysv/linux/raise.c:56
#2  0x76c29956 in __GI_abort () at abort.c:89
#3  0x76c22338 in __assert_fail_base (fmt=0x1 <error: Cannot access memory at address 0x1>, assertion=0x76984720 "isa<X>(Val) && \"cast_or_null<Ty>() argument of incompatible type!\"", assertion@entry=0x0, 
    file=0x769846d4 "/home/tbesard/julia/deps/srccache/llvm-3.7.0/include/llvm/Support/Casting.h", file@entry=0x76ff6000 "\001", line=269, line@entry=1993232564, 
    function=function@entry=0x769848b0 <llvm::cast_retty<llvm::MCSymbolELF, llvm::MCSymbol*>::ret_type llvm::cast_or_null<llvm::MCSymbolELF, llvm::MCSymbol>(llvm::MCSymbol*)::__PRETTY_FUNCTION__> "typename llvm::cast_retty<X, Y*>::ret_type llvm::cast_or_null(Y*) [with X = llvm::MCSymbolELF; Y = llvm::MCSymbol; typename llvm::cast_retty<X, Y*>::ret_type = llvm::MCSymbolELF*]") at assert.c:92
#4  0x76c223ce in __GI___assert_fail (assertion=0x0, file=0x76ff6000 "\001", line=1993232564, 
    function=0x769848b0 <llvm::cast_retty<llvm::MCSymbolELF, llvm::MCSymbol*>::ret_type llvm::cast_or_null<llvm::MCSymbolELF, llvm::MCSymbol>(llvm::MCSymbol*)::__PRETTY_FUNCTION__> "typename llvm::cast_retty<X, Y*>::ret_type llvm::cast_or_null(Y*) [with X = llvm::MCSymbolELF; Y = llvm::MCSymbol; typename llvm::cast_retty<X, Y*>::ret_type = llvm::MCSymbolELF*]") at assert.c:101
#5  0x75fe388a in llvm::cast_or_null<llvm::MCSymbolELF, llvm::MCSymbol> (Val=0xefa00) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/include/llvm/Support/Casting.h:269
#6  0x75fe22bc in llvm::MCELFStreamer::ChangeSection (this=0xa5220, Section=0xef888, Subsection=0x0) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/MC/MCELFStreamer.cpp:162
#7  0x75760468 in (anonymous namespace)::ARMELFStreamer::ChangeSection (this=0xa5220, Section=0xef888, Subsection=0x0)
    at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/Target/ARM/MCTargetDesc/ARMELFStreamer.cpp:445
#8  0x75ff7cbc in llvm::MCStreamer::SwitchSection (this=0xa5220, Section=0xef888, Subsection=0x0) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/MC/MCStreamer.cpp:706
#9  0x757612c2 in (anonymous namespace)::ARMTargetELFStreamer::finishAttributeSection (this=0xa5ac0) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/Target/ARM/MCTargetDesc/ARMELFStreamer.cpp:964
#10 0x7565f1dc in llvm::ARMAsmPrinter::emitAttributes (this=0xa5ff8) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/Target/ARM/ARMAsmPrinter.cpp:811
#11 0x7565df1c in llvm::ARMAsmPrinter::EmitStartOfAsmFile (this=0xa5ff8, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/Target/ARM/ARMAsmPrinter.cpp:438
#12 0x759b3338 in llvm::AsmPrinter::doInitialization (this=0xa5ff8, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/CodeGen/AsmPrinter/AsmPrinter.cpp:203
#13 0x75e34796 in llvm::FPPassManager::doInitialization (this=0x90b28, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/IR/LegacyPassManager.cpp:1549
#14 0x75e348ca in (anonymous namespace)::MPPassManager::runOnModule (this=0x85180, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/IR/LegacyPassManager.cpp:1581
#15 0x75e34e5e in llvm::legacy::PassManagerImpl::run (this=0x84f78, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/IR/LegacyPassManager.cpp:1698
#16 0x75e35012 in llvm::legacy::PassManager::run (this=0x84f20, M=...) at /home/tbesard/julia/deps/srccache/llvm-3.7.0/lib/IR/LegacyPassManager.cpp:1729
#17 0x76d95362 in JuliaOJIT::JuliaOJIT(llvm::TargetMachine&)::{lambda(llvm::Module&)#1}::operator()(llvm::Module&) const () at /home/tbesard/julia/src/jitlayers.cpp:283
#18 0x76ddf9f0 in std::_Function_handler<llvm::object::OwningBinary<llvm::object::ObjectFile> (llvm::Module&), JuliaOJIT::JuliaOJIT(llvm::TargetMachine&)::{lambda(llvm::Module&)#1}>::_M_invoke(std::_Any_data const&, llvm::Module&) (__functor=..., __args#0=...) at /usr/include/c++/4.8/functional:2057
#19 0x76de0dc6 in std::function<llvm::object::OwningBinary<llvm::object::ObjectFile> (llvm::Module&)>::operator()(llvm::Module&) const (this=0xa4a8c, __args#0=...) at /usr/include/c++/4.8/functional:2464
#20 0x76dd0de8 in llvm::orc::IRCompileLayer<llvm::orc::ObjectLinkingLayer<(anonymous namespace)::DebugObjectRegistrar> >::addModuleSet<llvm::SmallVector<std::unique_ptr<llvm::Module>, 1u>, llvm::RTDyldMemoryManager*, std::unique_ptr<llvm::orc::LambdaResolver<JuliaOJIT::addModule(llvm::Module*)::__lambda6, JuliaOJIT::addModule(llvm::Module*)::__lambda7>, std::default_delete<llvm::orc::LambdaResolver<JuliaOJIT::addModule(llvm::Module*)::__lambda6, JuliaOJIT::addModule(llvm::Module*)::__lambda7> > > >(llvm::SmallVector<std::unique_ptr<llvm::Module, std::default_delete<llvm::Module> >, 1u>, llvm::RTDyldMemoryManager *, std::unique_ptr<llvm::orc::LambdaResolver<JuliaOJIT::addModule(llvm::Module*)::__lambda6, JuliaOJIT::addModule(llvm::Module*)::__lambda7>, std::default_delete<llvm::orc::LambdaResolver<JuliaOJIT::addModule(llvm::Module*)::__lambda6, JuliaOJIT::addModule(llvm::Module*)::__lambda7> > >) (this=0xa4a88, Ms=..., MemMgr=0x85288, Resolver=...) at /home/tbesard/julia/usr/include/llvm/ExecutionEngine/Orc/IRCompileLayer.h:76
#21 0x76d95b5c in JuliaOJIT::addModule (this=0x83db8, M=0xe8110) at /home/tbesard/julia/src/jitlayers.cpp:348
#22 0x76da05a0 in jl_finalize_module (m=0xe8110) at /home/tbesard/julia/src/codegen.cpp:951
#23 0x76da0a04 in jl_generate_fptr (f=0x536259a0) at /home/tbesard/julia/src/codegen.cpp:1053
#24 0x76d4a662 in jl_trampoline (F=0x536259a0, args=0x7effea90, nargs=1) at /home/tbesard/julia/src/builtins.c:1035
#25 0x76d3ce64 in jl_apply (f=0x536259a0, args=0x7effea90, nargs=1) at /home/tbesard/julia/src/julia.h:1379
#26 0x76d41b10 in jl_apply_generic (F=0x535f7f20, args=0x7effea90, nargs=1) at /home/tbesard/julia/src/gf.c:1952
#27 0x5354e1e0 in julia.new_0 ()
#28 0x76d47234 in jl_apply (f=0x53625880, args=0x7effebcc, nargs=2) at /home/tbesard/julia/src/julia.h:1379
#29 0x76d4a66c in jl_trampoline (F=0x53625880, args=0x7effebcc, nargs=2) at /home/tbesard/julia/src/builtins.c:1036
#30 0x76d3ce64 in jl_apply (f=0x53625880, args=0x7effebcc, nargs=2) at /home/tbesard/julia/src/julia.h:1379
#31 0x76d41b10 in jl_apply_generic (F=0x53625840, args=0x7effebcc, nargs=2) at /home/tbesard/julia/src/gf.c:1952
#32 0x76d4f678 in jl_apply (f=0x53625840, args=0x7effebcc, nargs=2) at /home/tbesard/julia/src/julia.h:1379
#33 0x76d4fb12 in do_call (f=0x53625840, args=0x53628ff4, nargs=2, eval0=0x0, locals=0x0, nl=0, ngensym=0) at /home/tbesard/julia/src/interpreter.c:65
#34 0x76d50582 in eval (e=0x53625860, locals=0x0, nl=0, ngensym=0) at /home/tbesard/julia/src/interpreter.c:214
#35 0x76d4f878 in jl_interpret_toplevel_expr (e=0x53625860) at /home/tbesard/julia/src/interpreter.c:25
#36 0x76d69178 in jl_toplevel_eval_flex (e=0x53625850, fast=1) at /home/tbesard/julia/src/toplevel.c:531
#37 0x76d69484 in jl_parse_eval_all (fname=0x76e5fe28 "boot.jl", len=8) at /home/tbesard/julia/src/toplevel.c:581
#38 0x76d6966a in jl_load (fname=0x76e5fe28 "boot.jl", len=8) at /home/tbesard/julia/src/toplevel.c:621
#39 0x76d58a6c in _julia_init (rel=JL_IMAGE_JULIA_HOME) at /home/tbesard/julia/src/init.c:637
#40 0x76d5a0e6 in julia_init (rel=JL_IMAGE_JULIA_HOME) at /home/tbesard/julia/src/task.c:273
#41 0x0000aa3e in main (argc=1, argv=0x7efff5cc) at /home/tbesard/julia/ui/repl.c:625
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `bc1c18ec2f3452de4b5cb714191478e02bb3847a` and the full history behind it is present.
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
