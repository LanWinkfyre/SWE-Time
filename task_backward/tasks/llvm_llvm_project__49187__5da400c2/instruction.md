# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Polly)

|  |  |
| --- | --- |
| Bugzilla Link | [49843](https://llvm.org/bz49843) |
| Resolution | DUPLICATE |
| Resolved on | Apr 05, 2021 22:08 |
| Version | trunk |
| OS | Linux |
| CC | @tstellar |

## Extended Description 
cmake ../llvm -GNinja \
	-DLLVM_BUILD_LLVM_DYLIB=ON \
	-DLLVM_ENABLE_PROJECTS="polly" \
	-DLLVM_TARGETS_TO_BUILD="X86"
ninja lib/libLLVM-13git.so

Fails with:
[1468/1468] Linking CXX shared library lib/libLLVM-13git.so
FAILED: lib/libLLVM-13git.so
[build command redacted as it's very long]
ld.lld: error: undefined symbol: getPollyPluginInfo()
>>> referenced by Extension.def:2 (include/llvm/Support/Extension.def:2)
>>>               lib/Extensions/CMakeFiles/obj.LLVMExtensions.dir/Extensions.cpp.o:(llvm::details::extensions_anchor())
>>> referenced by Extension.def:2 (include/llvm/Support/Extension.def:2)
>>>               lib/LTO/CMakeFiles/obj.LLVMLTO.dir/LTOBackend.cpp.o:(RegisterPassPlugins(llvm::ArrayRef<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > >, llvm::PassBuilder&))



Observations:
* 
* Passing -DLLVM_POLLY_LINK_INTO_TOOLS=OFF works around the issue.

I've added some debug prints and confirmed that obj.Polly target is being created.
Dependency on Polly if it's static seems to be added in function(process_llvm_pass_plugins) to LLVMExtensions's LINK_LIBRARIES through LLVM_STATIC_EXTENSIONS.

I think the issue might be something to do with the fact if libLLVM is linked against obj.LLVMExtensions it doesn't pull in Polly as no linking happens for object libraries. But I'm not sure, as this is fairly complicated.
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `803b79221edfc2517e6bfc373e5f55609565b0e4` and the full history behind it is present.
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
