# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[clang] Crash at -O2: Assertion `all_of(I->users()... "during expansion"' failed.

This code crashes at `-O2`:

```c
int a, b, c, d;
void e() {
  int *f = 0;
  for (;;)
    for (; c - 100 + d <= b; d++) {
      f[d + a] = 1;
      a = 1 + c - 100;
    }
}
void main() {}
```

Compiler Explorer: https://godbolt.org/z/P3f6ef98P



Crash:

```console
clang: /root/llvm-project/llvm/lib/Transforms/Utils/ScalarEvolutionExpander.cpp:2402: void llvm::SCEVExpanderCleaner::cleanup(): Assertion `all_of(I->users(), [&InsertedSet](Value *U) { return InsertedSet.contains(cast<Instruction>(U)); }) && "removed instruction should only be used by instructions inserted " "during expansion"' failed.
```

Backtrace:

```c
Stack dump:
0.	Program arguments: /opt/compiler-explorer/clang-assertions-trunk/bin/clang -gdwarf-4 -g -o /app/output.s -mllvm --x86-asm-syntax=intel -fno-verbose-asm -S --gcc-toolchain=/opt/compiler-explorer/gcc-snapshot -fcolor-diagnostics -fno-crash-diagnostics -O2 -Wall -Wextra <source>
1.	<eof> parser at end of file
2.	Optimizer
3.	Running pass "function<eager-inv>(float2int,lower-constant-intrinsics,loop(loop-rotate<header-duplication;no-prepare-for-lto>,loop-deletion),loop-distribute,inject-tli-mappings,loop-vectorize<no-interleave-forced-only;no-vectorize-forced-only;>,infer-alignment,loop-load-elim,instcombine<max-iterations=1;no-verify-fixpoint>,simplifycfg<bonus-inst-threshold=1;forward-switch-cond;switch-range-to-icmp;switch-to-lookup;no-keep-loops;hoist-common-insts;no-hoist-loads-stores-with-cond-faulting;sink-common-insts;speculate-blocks;simplify-cond-branch;no-speculate-unpredictables>,slp-vectorizer,vector-combine,instcombine<max-iterations=1;no-verify-fixpoint>,loop-unroll<O2>,transform-warning,sroa<preserve-cfg>,infer-alignment,instcombine<max-iterations=1;no-verify-fixpoint>,loop-mssa(licm<allowspeculation>),alignment-from-assumptions,loop-sink,instsimplify,div-rem-pairs,tailcallelim,simplifycfg<bonus-inst-threshold=1;no-forward-switch-cond;switch-range-to-icmp;no-switch-to-lookup;keep-loops;no-hoist-common-insts;hoist-loads-stores-with-cond-faulting;no-sink-common-insts;speculate-blocks;simplify-cond-branch;speculate-unpredictables>)" on module "<source>"
4.	Running pass "loop-vectorize<no-interleave-forced-only;no-vectorize-forced-only;>" on function "e"
 #0 0x0000000003e7dc08 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3e7dc08)
 #1 0x0000000003e7b8c4 llvm::sys::CleanupOnSignal(unsigned long) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3e7b8c4)
 #2 0x0000000003dc0618 CrashRecoverySignalHandler(int) CrashRecoveryContext.cpp:0:0
 #3 0x00007507d4042520 (/lib/x86_64-linux-gnu/libc.so.6+0x42520)
 #4 0x00007507d40969fc pthread_kill (/lib/x86_64-linux-gnu/libc.so.6+0x969fc)
 #5 0x00007507d4042476 gsignal (/lib/x86_64-linux-gnu/libc.so.6+0x42476)
 #6 0x00007507d40287f3 abort (/lib/x86_64-linux-gnu/libc.so.6+0x287f3)
 #7 0x00007507d402871b (/lib/x86_64-linux-gnu/libc.so.6+0x2871b)
 #8 0x00007507d4039e96 (/lib/x86_64-linux-gnu/libc.so.6+0x39e96)
 #9 0x0000000003fea367 llvm::SCEVExpanderCleaner::cleanup() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3fea367)
#10 0x000000000597bc1f (anonymous namespace)::GeneratedRTChecks::~GeneratedRTChecks() LoopVectorize.cpp:0:0
#11 0x00000000059d28c8 llvm::LoopVectorizePass::processLoop(llvm::Loop*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x59d28c8)
#12 0x00000000059d4e29 llvm::LoopVectorizePass::runImpl(llvm::Function&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x59d4e29)
#13 0x00000000059d54a3 llvm::LoopVectorizePass::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x59d54a3)
#14 0x00000000055481fe llvm::detail::PassModel<llvm::Function, llvm::LoopVectorizePass, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x55481fe)
#15 0x000000000381c880 llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x381c880)
#16 0x00000000011a852e llvm::detail::PassModel<llvm::Function, llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x11a852e)
#17 0x000000000381b19b llvm::ModuleToFunctionPassAdaptor::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x381b19b)
#18 0x00000000011a764e llvm::detail::PassModel<llvm::Module, llvm::ModuleToFunctionPassAdaptor, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x11a764e)
#19 0x000000000381aba0 llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x381aba0)
#20 0x000000000412e684 (anonymous namespace)::EmitAssemblyHelper::RunOptimizationPipeline(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>&, std::unique_ptr<llvm::ToolOutputFile, std::default_delete<llvm::ToolOutputFile>>&, clang::BackendConsumer*) BackendUtil.cpp:0:0
#21 0x0000000004132031 clang::emitBackendOutput(clang::CompilerInstance&, clang::CodeGenOptions&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>, clang::BackendConsumer*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4132031)
#22 0x0000000004837120 clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4837120)
#23 0x000000000643be7c clang::ParseAST(clang::Sema&, bool, bool) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x643be7c)
#24 0x0000000004837528 clang::CodeGenAction::ExecuteAction() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4837528)
#25 0x0000000004b00005 clang::FrontendAction::Execute() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4b00005)
#26 0x0000000004a8398e clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4a8398e)
#27 0x0000000004bedf9e clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4bedf9e)
#28 0x0000000000d5391f cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xd5391f)
#29 0x0000000000d4b2da ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#30 0x000000000487fa49 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const::'lambda'()>(long) Job.cpp:0:0
#31 0x0000000003dc0ac4 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3dc0ac4)
#32 0x000000000488003f clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const (.part.0) Job.cpp:0:0
#33 0x00000000048426fd clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x48426fd)
#34 0x000000000484377e clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x484377e)
#35 0x000000000484b695 clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x484b695)
#36 0x0000000000d5076c clang_main(int, char**, llvm::ToolContext const&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xd5076c)
#37 0x0000000000c17ff4 main (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xc17ff4)
#38 0x00007507d4029d90 (/lib/x86_64-linux-gnu/libc.so.6+0x29d90)
#39 0x00007507d4029e40 __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x29e40)
#40 0x0000000000d4ad85 _start (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xd4ad85)
```
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `8727097ffd017ce55f39a3b7bc3788c6073e853d` and the full history behind it is present.
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
