# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash @llvm::InstCombinerImpl::sinkNotIntoOtherHandOfLogicalOp



Command line: `clang "-cc1" "-triple" "x86_64-unknown-linux-gnu" "-emit-obj" "--mrelax-relocations" "-disable-free" "-clear-ast-before-backend" "-disable-llvm-verifier" "-discard-value-names" "-main-file-name" "TestNsRefPtr.cpp" "-mrelocation-model" "pic" "-pic-level" "2" "-fhalf-no-semantic-interposition" "-mframe-pointer=all" "-relaxed-aliasing" "-ffp-contract=off" "-fno-rounding-math" "-mconstructor-aliases" "-funwind-tables=2" "-target-cpu" "x86-64" "-tune-cpu" "generic" "-mllvm" "-treat-scalable-fixed-error-as-warning" "-debug-info-kind=line-tables-only" "-dwarf-version=4" "-debugger-tuning=gdb" "-ffunction-sections" "-fdata-sections" "-sys-header-deps" "-O2" "-Wall" "-Wformat-security" "-fdeprecated-macro" "-fdebug-compilation-dir=/builds/worker/workspace/obj-build/xpcom/tests/gtest" "-ferror-limit" "19" "-fsanitize=address,array-bounds,bool,enum,function,integer-divide-by-zero,object-size,pointer-overflow,return,vla-bound,local-bounds" "-fno-sanitize-memory-param-retval" "-fsanitize-address-use-after-scope" "-fno-assume-sane-operator-new" "-pthread" "-fno-rtti" "-fgnuc-version=4.2.1" "-fno-aligned-allocation" "-vectorize-loops" "-vectorize-slp" "-faddrsig" "-x" "c++" "testcase.cpp"`

(I'm running creduce on the source, I'll provide the result of that when it's done)

Stack trace:
```
 #0 0x00007f38e18619e7 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) /tmp/llvm/llvm/lib/Support/Unix/Signals.inc:567:13
 #1 0x00007f38e185fd10 llvm::sys::RunSignalHandlers() /tmp/llvm/llvm/lib/Support/Signals.cpp:105:18
 #2 0x00007f38e186219f SignalHandler(int) /tmp/llvm/llvm/lib/Support/Unix/Signals.inc:412:1
 #3 0x00007f38e83c8140 __restore_rt (/lib/x86_64-linux-gnu/libpthread.so.0+0x13140)
 #4 0x00007f38e18f2dd7 llvm::Instruction::getParent() /tmp/llvm/llvm/include/llvm/IR/Instruction.h:91:55
 #5 0x00007f38e18f2dd7 llvm::IRBuilderBase::SetInsertPoint(llvm::Instruction*) /tmp/llvm/llvm/include/llvm/IR/IRBuilder.h:188:13
 #6 0x00007f38e24e0b01 llvm::InstCombinerImpl::sinkNotIntoOtherHandOfLogicalOp(llvm::Instruction&) /tmp/llvm/llvm/lib/Transforms/InstCombine/InstCombineAndOrXor.cpp:3747:7
 #7 0x00007f38e2561bd6 llvm::InstCombinerImpl::visitSelectInst(llvm::SelectInst&) /tmp/llvm/llvm/lib/Transforms/InstCombine/InstCombineSelect.cpp:0:7
 #8 0x00007f38e24bd850 llvm::InstCombinerImpl::run() /tmp/llvm/llvm/lib/Transforms/InstCombine/InstructionCombining.cpp:0:31
 #9 0x00007f38e24bee75 combineInstructionsOverFunction(llvm::Function&, llvm::InstructionWorklist&, llvm::AAResults*, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::TargetTransformInfo&, llvm::DominatorTree&, llvm::OptimizationRemarkEmitter&, llvm::BlockFrequencyInfo*, llvm::ProfileSummaryInfo*, unsigned int, llvm::LoopInfo*) /tmp/llvm/llvm/lib/Transforms/InstCombine/InstructionCombining.cpp:0:13
#10 0x00007f38e24bea76 llvm::InstCombinePass::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) /tmp/llvm/llvm/lib/Transforms/InstCombine/InstructionCombining.cpp:4635:8
#11 0x00007f38e6dd9f4d llvm::detail::PassModel<llvm::Function, llvm::InstCombinePass, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#12 0x00007f38e19bf007 void llvm::PassInstrumentation::runAfterPass<llvm::Function, llvm::detail::PassConcept<llvm::Function, llvm::AnalysisManager<llvm::Function>>>(llvm::detail::PassConcept<llvm::Function, llvm::AnalysisManager<llvm::Function>> const&, llvm::Function const&, llvm::PreservedAnalyses const&) const /tmp/llvm/llvm/include/llvm/IR/PassInstrumentation.h:256:9
#13 0x00007f38e19bf007 llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) /tmp/llvm/llvm/include/llvm/IR/PassManager.h:521:10
#14 0x00007f38e3598d4d llvm::detail::PassModel<llvm::Function, llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#15 0x00007f38e2a7d70f void llvm::PassInstrumentation::runAfterPass<llvm::Function, llvm::detail::PassConcept<llvm::Function, llvm::AnalysisManager<llvm::Function>>>(llvm::detail::PassConcept<llvm::Function, llvm::AnalysisManager<llvm::Function>> const&, llvm::Function const&, llvm::PreservedAnalyses const&) const /tmp/llvm/llvm/include/llvm/IR/PassInstrumentation.h:256:9
#16 0x00007f38e2a7d70f llvm::CGSCCToFunctionPassAdaptor::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/lib/Analysis/CGSCCPassManager.cpp:542:8
#17 0x00007f38e359a49d llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::CGSCCToFunctionPassAdaptor, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#18 0x00007f38e2a7a6bb llvm::PassManager<llvm::LazyCallGraph::SCC, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/lib/Analysis/CGSCCPassManager.cpp:89:12
#19 0x00007f38e284ed2d llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::PassManager<llvm::LazyCallGraph::SCC, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#20 0x00007f38e2a7c376 llvm::DevirtSCCRepeatedPass::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/lib/Analysis/CGSCCPassManager.cpp:411:12
#21 0x00007f38e284f3ed llvm::detail::PassModel<llvm::LazyCallGraph::SCC, llvm::DevirtSCCRepeatedPass, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&>::run(llvm::LazyCallGraph::SCC&, llvm::AnalysisManager<llvm::LazyCallGraph::SCC, llvm::LazyCallGraph&>&, llvm::LazyCallGraph&, llvm::CGSCCUpdateResult&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#22 0x00007f38e2a7ba93 llvm::ModuleToPostOrderCGSCCPassAdaptor::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/lib/Analysis/CGSCCPassManager.cpp:279:18
#23 0x00007f38e284f21d llvm::detail::PassModel<llvm::Module, llvm::ModuleToPostOrderCGSCCPassAdaptor, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#24 0x00007f38e19bddf7 void llvm::PassInstrumentation::runAfterPass<llvm::Module, llvm::detail::PassConcept<llvm::Module, llvm::AnalysisManager<llvm::Module>>>(llvm::detail::PassConcept<llvm::Module, llvm::AnalysisManager<llvm::Module>> const&, llvm::Module const&, llvm::PreservedAnalyses const&) const /tmp/llvm/llvm/include/llvm/IR/PassInstrumentation.h:256:9
#25 0x00007f38e19bddf7 llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/include/llvm/IR/PassManager.h:521:10
#26 0x00007f38e284be23 llvm::SmallPtrSetImplBase::isSmall() const /tmp/llvm/llvm/include/llvm/ADT/SmallPtrSet.h:195:33
#27 0x00007f38e284be23 llvm::SmallPtrSetImplBase::~SmallPtrSetImplBase() /tmp/llvm/llvm/include/llvm/ADT/SmallPtrSet.h:83:10
#28 0x00007f38e284be23 llvm::PreservedAnalyses::~PreservedAnalyses() /tmp/llvm/llvm/include/llvm/IR/PassManager.h:152:7
#29 0x00007f38e284be23 llvm::ModuleInlinerWrapperPass::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/lib/Transforms/IPO/Inliner.cpp:1171:3
#30 0x00007f38e43a672d llvm::detail::PassModel<llvm::Module, llvm::ModuleInlinerWrapperPass, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/include/llvm/IR/PassManagerInternal.h:89:5
#31 0x00007f38e19bddf7 void llvm::PassInstrumentation::runAfterPass<llvm::Module, llvm::detail::PassConcept<llvm::Module, llvm::AnalysisManager<llvm::Module>>>(llvm::detail::PassConcept<llvm::Module, llvm::AnalysisManager<llvm::Module>> const&, llvm::Module const&, llvm::PreservedAnalyses const&) const /tmp/llvm/llvm/include/llvm/IR/PassInstrumentation.h:256:9
#32 0x00007f38e19bddf7 llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) /tmp/llvm/llvm/include/llvm/IR/PassManager.h:521:10
#33 0x00007f38e6dd364c llvm::SmallPtrSetImplBase::isSmall() const /tmp/llvm/llvm/include/llvm/ADT/SmallPtrSet.h:195:33
#34 0x00007f38e6dd364c llvm::SmallPtrSetImplBase::~SmallPtrSetImplBase() /tmp/llvm/llvm/include/llvm/ADT/SmallPtrSet.h:83:10
#35 0x00007f38e6dd364c llvm::PreservedAnalyses::~PreservedAnalyses() /tmp/llvm/llvm/include/llvm/IR/PassManager.h:152:7
#36 0x00007f38e6dd364c (anonymous namespace)::EmitAssemblyHelper::RunOptimizationPipeline(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>&, std::unique_ptr<llvm::ToolOutputFile, std::default_delete<llvm::ToolOutputFile>>&) /tmp/llvm/clang/lib/CodeGen/BackendUtil.cpp:1059:5
#37 0x00007f38e6dcb205 (anonymous namespace)::EmitAssemblyHelper::EmitAssembly(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) /tmp/llvm/clang/lib/CodeGen/BackendUtil.cpp:0:3
#38 0x00007f38e6dcb205 clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) /tmp/llvm/clang/lib/CodeGen/BackendUtil.cpp:1275:13
#39 0x00007f38e71082ba std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>::~unique_ptr() /usr/lib/gcc/x86_64-linux-gnu/10/../../../../include/c++/10/bits/unique_ptr.h:360:6
#40 0x00007f38e71082ba clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) /tmp/llvm/clang/lib/CodeGen/CodeGenAction.cpp:381:7
#41 0x00007f38e5fa4b1e __gnu_cxx::__normal_iterator<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>*, std::vector<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>, std::allocator<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>>>>::__normal_iterator(std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>* const&) /usr/lib/gcc/x86_64-linux-gnu/10/../../../../include/c++/10/bits/stl_iterator.h:979:20
#42 0x00007f38e5fa4b1e std::vector<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>, std::allocator<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>>>::begin() /usr/lib/gcc/x86_64-linux-gnu/10/../../../../include/c++/10/bits/stl_vector.h:812:16
#43 0x00007f38e5fa4b1e void clang::finalize<std::vector<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>, std::allocator<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>>>>(std::vector<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>, std::allocator<std::unique_ptr<clang::TemplateInstantiationCallback, std::default_delete<clang::TemplateInstantiationCallback>>>>&, clang::Sema const&) /tmp/llvm/clang/include/clang/Sema/TemplateInstCallback.h:54:16
#44 0x00007f38e5fa4b1e clang::ParseAST(clang::Sema&, bool, bool) /tmp/llvm/clang/lib/Parse/ParseAST.cpp:203:3
#45 0x00007f38e79d3a38 clang::FrontendAction::Execute() /tmp/llvm/clang/lib/Frontend/FrontendAction.cpp:1059:10
#46 0x00007f38e7955b26 llvm::Error::getPtr() const /tmp/llvm/llvm/include/llvm/Support/Error.h:275:12
#47 0x00007f38e7955b26 llvm::Error::operator bool() /tmp/llvm/llvm/include/llvm/Support/Error.h:235:16
#48 0x00007f38e7955b26 clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) /tmp/llvm/clang/lib/Frontend/CompilerInstance.cpp:1046:23
#49 0x00007f38e7a47960 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) /tmp/llvm/clang/lib/FrontendTool/ExecuteCompilerInvocation.cpp:264:25
#50 0x000055b33231e206 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) /tmp/llvm/clang/tools/driver/cc1_main.cpp:251:15
#51 0x000055b33231ba1c ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&) /tmp/llvm/clang/tools/driver/driver.cpp:353:12
#52 0x000055b33231b6b9 clang_main(int, char**) /tmp/llvm/clang/tools/driver/driver.cpp:429:12
#53 0x00007f38ddbe7d0a __libc_start_main ./csu/../csu/libc-start.c:308:16
#54 0x000055b3323183da _start (/tmp/llvm/obj2/bin/clang+0xf3da)
```

Cc: @LebedevRI
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `b6e344ce91c8796331fca7644eb8c748ac5391ec` and the full history behind it is present.
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
