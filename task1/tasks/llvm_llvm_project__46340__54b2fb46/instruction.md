# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
bug in code generation for aarch64 target reg-to-reg copy

|  |  |
| --- | --- |
| Bugzilla Link | [46996](https://llvm.org/bz46996) |
| Resolution | FIXED |
| Resolved on | Jun 28, 2021 06:25 |
| Version | 10.0 |
| OS | All |
| CC | @Arnaud-de-Grandmaison-ARM,@DavidSpickett,@smithp35 |

## Extended Description 
Compile with assertions enabled and then try following reproducer:

```
; ModuleID = 'simplified.ll'
source_filename = "<string>"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "aarch64-linux-gnu"
define [3 x { double, i1 }] @"broken"() local_unnamed_addr #&#8203;0 {
entry:
  ret [3 x { double, i1 }] zeroinitializer
}
```

Then reproduce with:

```
llc -march=aarch64 simplified.ll                                                                                                
unimplemented reg-to-reg copy
UNREACHABLE executed at /Users/vhaenel/git/llvm-project/llvm/lib/Target/AArch64/AArch64InstrInfo.cpp:2818!
Stack dump:
0.	Program arguments: git/llvm-build-10.0.1/bin/llc -march=aarch64 simplified.ll
1.	Running pass 'Function Pass Manager' on module 'simplified.ll'.
2.	Running pass 'Post-RA pseudo instruction expansion pass' on function '@broken'
0  llc                      0x0000000106fe4058 llvm::sys::PrintStackTrace(llvm::raw_ostream&) + 40
1  llc                      0x0000000106fe2df8 llvm::sys::RunSignalHandlers() + 248
2  llc                      0x0000000106fe466d SignalHandler(int) + 285
3  libsystem_platform.dylib 0x00007fff7200f5fd _sigtramp + 29
4  libsystem_platform.dylib 0x000000000000004c _sigtramp + 18446603338603498092
5  libsystem_c.dylib        0x00007fff71ee5808 abort + 120
6  llc                      0x0000000107aaf68e llvm::llvm_unreachable_internal(char const*, char const*, unsigned int) + 462
7  llc                      0x000000010600f8a8 llvm::AArch64InstrInfo::copyPhysReg(llvm::MachineBasicBlock&, llvm::MachineInstrBundleIterator<llvm::MachineInstr, false>, llvm::DebugLoc const&, llvm::MCRegister, llvm::MCRegister, bool) const + 6856
8  llc                      0x000000010647758e (anonymous namespace)::ExpandPostRA::runOnMachineFunction(llvm::MachineFunction&) + 2942
9  llc                      0x000000010656555d llvm::MachineFunctionPass::runOnFunction(llvm::Function&) + 349
10 llc                      0x00000001068e7928 llvm::FPPassManager::runOnFunction(llvm::Function&) + 1064
11 llc                      0x00000001068e7bf8 llvm::FPPassManager::runOnModule(llvm::Module&) + 72
12 llc                      0x00000001068e80f2 llvm::legacy::PassManagerImpl::run(llvm::Module&) + 1026
13 llc                      0x0000000105aabf53 compileModule(char**, llvm::LLVMContext&) + 9219
14 llc                      0x0000000105aa97bc main + 1404
15 libdyld.dylib            0x00007fff71e16cc9 start + 1
[1]    3621 abort (core dumped)  git/llvm-build-10.0.1/bin/llc -march=aarch64 simplified.ll
git/llvm-build-10.0.1/bin/llc -march=aarch64 simplified.ll  0.02s user 9.80s system 47% cpu 20.569 tot
```

No problem! This reproducer is all that's needed, you got it right first time.





> This bug is currently blocking an upgrade of our Aarch64 support from LLVM 9 -> LLVM 11.
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `e8b7edafc3dd0ab85903eebdfdb3bb7cc2d66743` and the full history behind it is present.
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
