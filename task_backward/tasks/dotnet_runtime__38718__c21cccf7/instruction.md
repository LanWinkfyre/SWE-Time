# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Mono perf regression based on TechEmpower PlaintextPlatform benchmark

Recently, there is a ~5% regression on TechEmpower PlaintextPlatform benchmark for all 3 different flavors of mono (JIT, LLVM JIT, LLVM AOT)



For mono JIT, with the commit before this one, RPS (requests per second) was 9,173,356; with this commit, RPS was 8,709,109. For LLVM JIT and LLVM AOT, the regression percentage was similar. For LLVM AOT, the number went from 10,244,296 to 9,795,509.

To get the results from your own machine:
1. Clone https://github.com/aspnet/Benchmarks
2. cd Benchmarks/src/BenchmarksDriver2
3. dotnet run -- --config ../BenchmarksApps/Kestrel/PlatformBenchmarks/platform.benchmarks.yml --scenario plaintext --profile aspnet-citrine-lin --application.selfContained true --application.runtimeVersion 5.0.0-preview.8.20324.2 -i 3 --application.options.outputFiles path_to/System.Private.CoreLib.dll --application.options.outputFiles path_to/libcoreclr.so

* Note that System.Private.CoreLib.dll and libcoreclr.so should comes from linux build. They usually live at
artifacts/obj/mono/Linux.x64.Release/mono/mini/.libs/libmonosgen-2.0.so (needs to be rename to libcoreclr.so)
artifacts/bin/mono/Linux.x64.Release/System.Private.CoreLib.dll


/cc @tannergooding @imhameed
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `106cd9ebaed5f974fa8f17e153ec3e22b6576f43` and the full history behind it is present.
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
