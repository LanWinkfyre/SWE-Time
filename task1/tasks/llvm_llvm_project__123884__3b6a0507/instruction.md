# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[clang] Crash at -O1

This code crashes at `-O1`:

```c
int a, b, c;
unsigned char d;
short e;
int f(long g, int h) {
  switch (b) {
  case 2:
    return g;
  default:
    return *(int *)(h + g * sizeof(int));
  }
}
void i(long);
void j() {
  e = d >> a;
  i(e);
}
void i(long g) { c = f(g + 4, g); }
int main() {}
```

Compiler Explorer: https://godbolt.org/z/6dWc1cPcb 



No crash info. 

Backtrace:

```console
0.	Program arguments: /opt/compiler-explorer/clang-trunk/bin/clang -gdwarf-4 -g -o /app/output.s -mllvm --x86-asm-syntax=intel -fno-verbose-asm -S --gcc-toolchain=/opt/compiler-explorer/gcc-snapshot -fcolor-diagnostics -fno-crash-diagnostics -O1 -Wall -Wextra <source>
1.	<eof> parser at end of file
2.	Code generation
3.	Running pass 'Function Pass Manager' on module '<source>'.
4.	Running pass 'Live Variable Analysis' on function '@j'
 #0 0x0000000003a8ded8 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/compiler-explorer/clang-trunk/bin/clang+0x3a8ded8)
 #1 0x0000000003a8c024 llvm::sys::CleanupOnSignal(unsigned long) (/opt/compiler-explorer/clang-trunk/bin/clang+0x3a8c024)
 #2 0x00000000039db3a8 CrashRecoverySignalHandler(int) CrashRecoveryContext.cpp:0:0
 #3 0x000070a531442520 (/lib/x86_64-linux-gnu/libc.so.6+0x42520)
 #4 0x0000000002dff8eb llvm::LiveVariables::HandleVirtRegUse(llvm::Register, llvm::MachineBasicBlock*, llvm::MachineInstr&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x2dff8eb)
 #5 0x0000000002e0000c llvm::LiveVariables::runOnInstr(llvm::MachineInstr&, llvm::SmallVectorImpl<llvm::Register>&, unsigned int) (/opt/compiler-explorer/clang-trunk/bin/clang+0x2e0000c)
 #6 0x0000000002e00bf4 llvm::LiveVariables::runOnBlock(llvm::MachineBasicBlock*, unsigned int) (/opt/compiler-explorer/clang-trunk/bin/clang+0x2e00bf4)
 #7 0x0000000002e01b22 llvm::LiveVariables::analyze(llvm::MachineFunction&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x2e01b22)
 #8 0x0000000002e01f6d llvm::LiveVariablesWrapperPass::runOnMachineFunction(llvm::MachineFunction&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x2e01f6d)
 #9 0x0000000002e9acd5 llvm::MachineFunctionPass::runOnFunction(llvm::Function&) (.part.0) MachineFunctionPass.cpp:0:0
#10 0x00000000033f3f82 llvm::FPPassManager::runOnFunction(llvm::Function&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x33f3f82)
#11 0x00000000033f4211 llvm::FPPassManager::runOnModule(llvm::Module&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x33f4211)
#12 0x00000000033f5b79 llvm::legacy::PassManagerImpl::run(llvm::Module&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x33f5b79)
#13 0x0000000003d30a85 clang::emitBackendOutput(clang::CompilerInstance&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>, clang::BackendConsumer*) (/opt/compiler-explorer/clang-trunk/bin/clang+0x3d30a85)
#14 0x00000000043d90e8 clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x43d90e8)
#15 0x000000000630885c clang::ParseAST(clang::Sema&, bool, bool) (/opt/compiler-explorer/clang-trunk/bin/clang+0x630885c)
#16 0x00000000043d9805 clang::CodeGenAction::ExecuteAction() (/opt/compiler-explorer/clang-trunk/bin/clang+0x43d9805)
#17 0x00000000046b3341 clang::FrontendAction::Execute() (/opt/compiler-explorer/clang-trunk/bin/clang+0x46b3341)
#18 0x0000000004632d6b clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x4632d6b)
#19 0x000000000479d933 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/compiler-explorer/clang-trunk/bin/clang+0x479d933)
#20 0x0000000000d10521 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/compiler-explorer/clang-trunk/bin/clang+0xd10521)
#21 0x0000000000d08d1d ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#22 0x0000000004425109 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const::'lambda'()>(long) Job.cpp:0:0
#23 0x00000000039db7d3 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (/opt/compiler-explorer/clang-trunk/bin/clang+0x39db7d3)
#24 0x0000000004425329 clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const (.part.0) Job.cpp:0:0
#25 0x00000000043e942d clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const (/opt/compiler-explorer/clang-trunk/bin/clang+0x43e942d)
#26 0x00000000043ea3c1 clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const (/opt/compiler-explorer/clang-trunk/bin/clang+0x43ea3c1)
#27 0x00000000043f475c clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) (/opt/compiler-explorer/clang-trunk/bin/clang+0x43f475c)
#28 0x0000000000d0d1b1 clang_main(int, char**, llvm::ToolContext const&) (/opt/compiler-explorer/clang-trunk/bin/clang+0xd0d1b1)
#29 0x0000000000bd37f4 main (/opt/compiler-explorer/clang-trunk/bin/clang+0xbd37f4)
#30 0x000070a531429d90 (/lib/x86_64-linux-gnu/libc.so.6+0x29d90)
#31 0x000070a531429e40 __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x29e40)
#32 0x0000000000d087b5 _start (/opt/compiler-explorer/clang-trunk/bin/clang+0xd087b5)
```
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `65df99c208ed40271f6dcdfc29bed56540467ce7` and the full history behind it is present.
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
