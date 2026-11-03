# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
macOS: Julia hangs if `ENABLE_GDBLISTENER=1` is set

```
$ export ENABLE_GDBLISTENER=1

$ make
...
    JULIA usr/lib/julia/basecompiler-o.a
# hangs
```

```
Platform Info:
  OS: macOS (arm64-apple-darwin24.5.0)
  CPU: 12 × Apple M2 Max
  WORD_SIZE: 64
  LIBM: libopenlibm
  LLVM: libLLVM-15.0.7 (ORCJIT, apple-m1)
```

CC: @vtjnash 

Copying my findings from #59146:

We're blocked waiting on a condition variable (seemingly inside `std::promise`?) in `llvm::orc::GDBJITDebugInfoRegistrationPlugin::Create`:

```
(lldb) thread backtrace all
* thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGSTOP
  * frame #0: 0x0000000181dfc3cc libsystem_kernel.dylib`__psynch_cvwait + 8
    frame #1: 0x0000000181e3b0e0 libsystem_pthread.dylib`_pthread_cond_wait + 984
    frame #2: 0x0000000181d6b298 libc++.1.dylib`std::__1::condition_variable::wait(std::__1::unique_lock<std::__1::mutex>&) + 32
    frame #3: 0x0000000181d6b9bc libc++.1.dylib`std::__1::__assoc_sub_state::__sub_wait(std::__1::unique_lock<std::__1::mutex>&) + 48
    frame #4: 0x000000010cd9516c libLLVM.dylib`std::__1::__assoc_state<llvm::MSVCPExpected<llvm::DenseMap<llvm::orc::SymbolStringPtr, llvm::orc::ExecutorSymbolDef, llvm::DenseMapInfo<llvm::orc::SymbolStringPtr, void>, llvm::detail::DenseMapPair<llvm::orc::SymbolStringPtr, llvm::orc::ExecutorSymbolDef>>>>::move() + 60
    frame #5: 0x000000010cd77eec libLLVM.dylib`llvm::orc::ExecutionSession::lookup(std::__1::vector<std::__1::pair<llvm::orc::JITDylib*, llvm::orc::JITDylibLookupFlags>, std::__1::allocator<std::__1::pair<llvm::orc::JITDylib*, llvm::orc::JITDylibLookupFlags>>> const&, llvm::orc::SymbolLookupSet, llvm::orc::LookupKind, llvm::orc::SymbolState, std::__1::function<void (llvm::DenseMap<llvm::orc::JITDylib*, llvm::DenseSet<llvm::orc::SymbolStringPtr, llvm::DenseMapInfo<llvm::orc::SymbolStringPtr, void>>, llvm::DenseMapInfo<llvm::orc::JITDylib*, void>, llvm::detail::DenseMapPair<llvm::orc::JITDylib*, llvm::DenseSet<llvm::orc::SymbolStringPtr, llvm::DenseMapInfo<llvm::orc::SymbolStringPtr, void>>>> const&)>) + 572
    frame #6: 0x000000010cd781c0 libLLVM.dylib`llvm::orc::ExecutionSession::lookup(std::__1::vector<std::__1::pair<llvm::orc::JITDylib*, llvm::orc::JITDylibLookupFlags>, std::__1::allocator<std::__1::pair<llvm::orc::JITDylib*, llvm::orc::JITDylibLookupFlags>>> const&, llvm::orc::SymbolStringPtr, llvm::orc::SymbolState) + 432
    frame #7: 0x000000010cd78504 libLLVM.dylib`llvm::orc::ExecutionSession::lookup(llvm::ArrayRef<llvm::orc::JITDylib*>, llvm::orc::SymbolStringPtr, llvm::orc::SymbolState) + 132
    frame #8: 0x000000010ce6781c libLLVM.dylib`llvm::orc::GDBJITDebugInfoRegistrationPlugin::Create(llvm::orc::ExecutionSession&, llvm::orc::JITDylib&, llvm::Triple const&) + 332
    frame #9: 0x00000001065d4b58 libjulia-codegen-debug.1.13.0.dylib`JuliaOJIT::enableJITDebuggingSupport(this=0x0000000156009800) at jitlayers.cpp:2245:40
    frame #10: 0x00000001064e7094 libjulia-codegen-debug.1.13.0.dylib`::jl_init_llvm() at codegen.cpp:10152:29
    frame #11: 0x00000001064e729c libjulia-codegen-debug.1.13.0.dylib`::jl_init_codegen_impl() at codegen.cpp:10206:5
    frame #12: 0x0000000105121578 libjulia-internal-debug.1.13.0.dylib`_finish_jl_init_(sysimage=(kind = JL_IMAGE_KIND_NONE, pointers = 0x0000000000000000, data = 0x0000000000000000, size = 0, base = 0), ptls=0x000000015600aa00, ct=0x000000010ec28010) at init.c:582:5
    frame #13: 0x00000001051212e4 libjulia-internal-debug.1.13.0.dylib`ijl_init_(sysimage=(kind = JL_IMAGE_KIND_NONE, pointers = 0x0000000000000000, data = 0x0000000000000000, size = 0, base = 0)) at init.c:783:5
    frame #14: 0x00000001051791c4 libjulia-internal-debug.1.13.0.dylib`jl_repl_entrypoint(argc=5, argv=0x000000016b4cb1c0) at jlapi.c:1131:5
    frame #15: 0x0000000104970ff4 libjulia-debug.1.13.0.dylib`jl_load_repl(argc=15, argv=0x000000016b4cb1c0) at loader_lib.c:601:12
    frame #16: 0x00000001049346d4 julia-debug`main(argc=15, argv=0x000000016b4cb1c0) at loader_exe.c:58:15
    frame #17: 0x0000000181a9ab98 dyld`start + 6076
  thread #2
    frame #0: 0x0000000181dfed04 libsystem_kernel.dylib`kevent + 8
    frame #1: 0x000000010517cdf4 libjulia-internal-debug.1.13.0.dylib`signal_listener(arg=0x0000000000000000) at signals-unix.c:957:27
    frame #2: 0x0000000181e3ac0c libsystem_pthread.dylib`_pthread_start + 136
  thread #3
    frame #0: 0x0000000181df8c34 libsystem_kernel.dylib`mach_msg2_trap + 8
    frame #1: 0x0000000181e0b3a0 libsystem_kernel.dylib`mach_msg2_internal + 76
    frame #2: 0x0000000181e01764 libsystem_kernel.dylib`mach_msg_overwrite + 484
    frame #3: 0x0000000181e00b98 libsystem_kernel.dylib`mach_msg_server + 348
    frame #4: 0x000000010517b1e8 libjulia-internal-debug.1.13.0.dylib`mach_segv_listener(arg=0x0000000000000000) at signals-mach.c:155:15
    frame #5: 0x0000000181e3ac0c libsystem_pthread.dylib`_pthread_start + 136
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `c5ba4e28f2c9c49be01ed7409efedef8627fe96d` and the full history behind it is present.
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
