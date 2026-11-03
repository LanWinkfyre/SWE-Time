# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[DeadStoreElimination w/ MemSSA]  wrong code

|  |  |
| --- | --- |
| Bugzilla Link | [48036](https://llvm.org/bz48036) |
| Resolution | FIXED |
| Resolved on | Nov 01, 2020 03:12 |
| Version | trunk |
| OS | Linux |
| Attachments | [extracted function](https://user-images.githubusercontent.com/55128014/143761362-2fac08d6-c6f1-4713-8585-e1b3027f106e.gz) |
| CC | @alinas,@fhahn,@LebedevRI,@JonPsson,@uweigand |


## Extended Description 


This SystemZ multistage bot is failing since weeks: http://lab.llvm.org:8011/#/builders/8/builds/6. Stage-2 llvm-objcopy has a corrupt size value which causes a call to fallocate of an insane amount which causes the abortion:

llvm-objcopy --decompress-debug-sections ./build-multistage/test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmpz.o ./build-multistage/test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmp2.o
llvm-objcopy: error: ... No space left on device

This is the llvm-objcopy compiled by clang (which was compiled by gcc).

 I narrowed it all down to one file (llvm-objcopy/ELF/Object.cpp) and function to the point where I think I can see just one store being DSE:ed in a function which seems to be incorrect.

To build:
1:
build as usual in $BUILD

2:
mkdir stage2
cd stage2
cmake -G Ninja ../llvm-project/llvm -DCMAKE_C_COMPILER=$BUILD/bin/clang -DCMAKE_CXX_COMPILER=$BUILD/bin/clang++ -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_ASSERTIONS=On
ninja check

/bin/llvm-objcopy --decompress-debug-sections ./test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmpz.o ./test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmp2.o
./bin/llvm-objcopy: error: './test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmpz.o': './test/tools/llvm-objcopy/ELF/Output/compress-debug-sections.test.tmp2.o': No space left on device

I found that if I recompiled ELF/Object.cpp with these options the error disappears:

-mllvm -enable-dse-partial-store-merging=false -mllvm -dse-memoryssa-defs-per-block-limit=3 -mllvm -dse-memoryssa-path-check-limit=1 -mllvm -dse-memoryssa-partial-store-limit=1 -mllvm -dse-memoryssa-scanlimit=19 -mllvm -dse-memoryssa-walklimit=85

Changing the last option to '86' instead produces the bad code again...

I found that it was enough to replace this function in Object.bc: _ZN4llvm7objcopy3elf10ELFBuilderINS_6object7ELFTypeILNS_7support10endiannessE1ELb1EEEE11makeSectionERKNS3_13Elf_Shdr_ImplIS7_EE

I managed then to extract the right function and run with opt instead:

./bin/opt -mtriple=s390x-linux-gnu fun.ll -S -o out.opt.86.ll -basic-aa -aa -memoryssa -dse -enable-dse-partial-overwrite-tracking=false -enable-dse-partial-store-merging=false -dse-memoryssa-defs-per-block-limit=3 -dse-memoryssa-path-check-limit=1 -dse-memoryssa-partial-store-limit=1 -dse-memoryssa-scanlimit=19 -dse-memoryssa-walklimit=86 -debug-only=dse >& dbg86_opt

./bin/opt -mtriple=s390x-linux-gnu fun.ll -S -o out.opt.85.ll -basic-aa -aa -memoryssa -dse -enable-dse-partial-overwrite-tracking=false -enable-dse-partial-store-merging=false -dse-memoryssa-defs-per-block-limit=3 -dse-memoryssa-path-check-limit=1 -dse-memoryssa-partial-store-limit=1 -dse-memoryssa-scanlimit=19 -dse-memoryssa-walklimit=85 -debug-only=dse >& dbg85_opt

diff dbg85_opt dbg86_opt | grep "DSE: Remove Dead Store" | ...
>     DSE: Remove Dead Store:

There is one more store eliminated, which seems wrong to me. It is the saving of the argument %DecompressedSize (:-)  which for some reason is removed:

define void @&#8203;_ZN4llvm7objcopy3elf17CompressedSection6createENS_8ArrayRefIhEEmm(... , i64 %DecompressedSize, ...) {

%ref.tmp = alloca %"class.llvm::objcopy::elf::CompressedSection", align 8
...
%DecompressedSize2.i = getelementptr inbounds %"class.llvm::objcopy::elf::CompressedSection", %"class.llvm::objcopy::elf::CompressedSection"* %ref.tmp, i64 0, i32 2
store i64 %DecompressedSize, i64* %DecompressedSize2.i, align 8, !tbaa !&#8203;26
...
}

I can't see any other store to that address/element, and I have no idea why DSE removes it...
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `799033d8c569616fbf7c829f2e9b01d5adf4cd6f` and the full history behind it is present.
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
